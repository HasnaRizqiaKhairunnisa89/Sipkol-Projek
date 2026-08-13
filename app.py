from datetime import datetime
import os
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------------------------------------------------------
# CONFIG & LOAD MODEL LANGSUNG
# -----------------------------------------------------------------------------
LOG_FILE = "logs.csv"

# Load Model & Vectorizer langsung di Streamlit
@st.cache_resource
def load_ai_model():
  model = joblib.load("model.pkl")
  vectorizer = joblib.load("vectorizer.pkl")
  return model, vectorizer


model, vectorizer = load_ai_model()

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

st.set_page_config(
    page_title="CivicReport AI Enterprise", page_icon="🏛️", layout="wide"
)

# ... (Taruh CSS Markdown Anda di sini) ...


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def predict_logic(text: str):
  text_lower = text.lower()
  x = vectorizer.transform([text])
  label = str(model.predict(x)[0])

  confidence = 85.0
  if hasattr(model, "predict_proba"):
    probs = model.predict_proba(x)[0]
    confidence = float(max(probs) * 100)

  if any(word in text_lower for word in HIGH_URGENCY_KEYWORDS):
    urgency = "🔴 DARURAT"
  elif len(text) > 150:
    urgency = "🟡 SEDANG"
  else:
    urgency = "🟢 NORMAL"

  return label, round(confidence, 2), urgency


# ... (Di bagian tombol 'btn_predict' ganti pemanggilan requests.post dengan predict_logic) ...
if btn_predict:
  actual_text = text_input.strip()
  if not actual_text:
    st.warning("Silakan isi teks aduan terlebih dahulu.")
  else:
    # Panggil fungsi prediksi langsung tanpa API
    label, confidence, urgency = predict_logic(actual_text)

    st.markdown(
        f'<div class="urgent-badge">Tingkat Prioritas: {urgency}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="badge-container"><div class="badge-title">Unit Kerja'
        f' Tujuan</div><div class="badge-value">{label}</div></div>',
        unsafe_allow_html=True,
    )

    # Simpan ke log...
    append_log(actual_text, label, confidence, urgency, pelapor_input, lokasi_input)
