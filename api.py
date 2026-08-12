from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI(title="CivicReport AI API", version="1.0")

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    x = vectorizer.transform([req.text])
    label = model.predict(x)[0]
    return PredictResponse(label=label)