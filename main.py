from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import re

app = FastAPI(title="CivicReport AI API", version="1.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Kata kunci untuk deteksi urgensi
HIGH_URGENCY_KEYWORDS = [
    "darurat", "bahaya", "ambruk", "kebakaran", "korban", 
    "kecelakaan", "banjir", "longsor", "patah", "meledak", "segera"
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
    text_lower = req.text.lower()
    x = vectorizer.transform([req.text])
    label = str(model.predict(x)[0])

    # Hitung Confidence Score
    confidence = 85.0
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x)[0]
        confidence = float(max(probs) * 100)

    # Deteksi Tingkat Urgensi
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
