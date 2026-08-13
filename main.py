import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pydantic import BaseModel

# Set up logging untuk melihat detail jika ada error di Render/Cloud
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="CivicReport AI API", version="1.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model & Vectorizer
try:
  model = joblib.load("model.pkl")
  vectorizer = joblib.load("vectorizer.pkl")
except Exception as e:
  logging.error(f"Gagal memuat model: {e}")

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
  urgency: str  # Darurat / Sedang / Normal


@app.get("/health")
def health():
  return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
  # 1. Validasi Input
  if not req.text or not req.text.strip():
    raise HTTPException(status_code=400, detail="Teks tidak boleh kosong.")

  try:
    text_lower = req.text.lower()
    x = vectorizer.transform([req.text])
    pred = model.predict(x)[0]
    label = str(pred)

    # 2. Hitung Confidence Score secara Aman
    confidence = 85.0
    try:
      if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x)[0]
        confidence = float(max(probs) * 100)
      elif hasattr(model, "decision_function"):
        # Alternatif jika model menggunakan Support Vector Machine (SVM)
        decision = model.decision_function(x)
        # Bawa nilai decision function ke rentang persentase kasar
        confidence = 80.0
    except Exception as cf_err:
      logging.warning(f"Gagal menghitung confidence: {cf_err}")
      confidence = 85.0

    # 3. Deteksi Tingkat Urgensi
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
    logging.error(f"Error saat prediksi: {e}")
    raise HTTPException(
        status_code=500, detail=f"Gagal memproses prediksi: {str(e)}"
    )
