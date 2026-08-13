import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pydantic import BaseModel

# Logging setup
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="CivicReport AI API", version="1.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model & Vectorizer secara aman
model = None
vectorizer = None

try:
  model = joblib.load("model.pkl")
  vectorizer = joblib.load("vectorizer.pkl")
  logging.info("Model dan Vectorizer berhasil dimuat.")
except Exception as e:
  logging.error(f"⚠️ Gagal memuat model/vectorizer: {e}")

# Kata kunci untuk deteksi urgensi
HIGH_URGENCY_KEYWORDS = [
    "darurat",
    "bahaya",
    "ambruk",
    "kebakaran",
    "korban",
    "kecelakaan",
    "banjir",
    "longsor",
    "patah",
    "meledak",
    "segera",
]


class PredictRequest(BaseModel):
  text: str


class PredictResponse(BaseModel):
  label: str
  confidence: float
  urgency: str


@app.get("/health")
def health():
  return {
      "status": "ok",
      "model_loaded": model is not None,
      "vectorizer_loaded": vectorizer is not None,
  }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
  # 1. Validasi Input
  if not req.text or not req.text.strip():
    raise HTTPException(status_code=400, detail="Teks tidak boleh kosong.")

  # 2. Cek Apakah Model & Vectorizer Tersedia
  if model is None or vectorizer is None:
    logging.error("Model atau Vectorizer belum dimuat di server.")
    raise HTTPException(
        status_code=500,
        detail=(
            "Model ML belum dimuat di server. Pastikan file 'model.pkl' dan"
            " 'vectorizer.pkl' sudah ada di repositori Render."
        ),
    )

  try:
    text_lower = req.text.lower()

    # Transformer & Predict
    x = vectorizer.transform([req.text])
    pred = model.predict(x)[0]
    label = str(pred)

    # 3. Hitung Confidence Score
    confidence = 85.0
    try:
      if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x)[0]
        confidence = float(max(probs) * 100)
      elif hasattr(model, "decision_function"):
        confidence = 80.0
    except Exception as cf_err:
      logging.warning(f"Gagal menghitung confidence: {cf_err}")

    # 4. Deteksi Tingkat Urgensi
    if any(word in text_lower for word in HIGH_URGENCY_KEYWORDS):
      urgency = "🔴 DARURAT"
    elif len(req.text) > 150:
      urgency = "🟡 SEDANG"
    else:
      urgency = "🟢 NORMAL"

    return PredictResponse(
        label=label, confidence=round(confidence, 2), urgency=urgency
    )

  except Exception as e:
    logging.error(f"Error saat memproses prediksi: {e}")
    raise HTTPException(
        status_code=500, detail=f"Gagal memproses prediksi: {str(e)}"
    )
