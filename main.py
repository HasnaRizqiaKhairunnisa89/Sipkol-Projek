import os
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="CivicReport AI API", version="1.2")

# Mengizinkan CORS agar frontend Streamlit bisa mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Kata kunci deteksi urgensi
HIGH_URGENCY_KEYWORDS = [
    "darurat", "bahaya", "ambruk", "kebakaran", "korban", 
    "kecelakaan", "banjir", "longsor", "patah", "meledak", "segera"
]

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    confidence: float
    urgency: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    text_lower = req.text.lower()
    x = vectorizer.transform([req.text])
    label = str(model.predict(x)[0])

    confidence = 85.0
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x)[0]
        confidence = float(max(probs) * 100)

    if any(word in text_lower for word in HIGH_URGENCY_KEYWORDS):
        urgency = "🔴 DARURAT"
    elif len(req.text) > 150:
        urgency = "🟡 SEDANG"
    else:
        urgency = "🟢 NORMAL"

    return PredictResponse(
        label=label, 
        confidence=round(confidence, 2),
        urgency=urgency
    )

if __name__ == "__main__":
    import uvicorn
    # Membaca PORT dari environment variable server hosting (default: 8000)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
