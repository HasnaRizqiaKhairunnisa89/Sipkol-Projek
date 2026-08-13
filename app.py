import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# -----------------------------------------------------------------------------
# CONFIG & CONSTANTS
# -----------------------------------------------------------------------------
API_URL = "https://project-skpi.onrender.com/predict"
LOG_FILE = "logs.csv"

st.set_page_config(
    page_title="CivicReport",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .main { background-color: #F8FAFC; }
    .header-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .header-card h1 { font-size: 2.2rem; font-weight: 800; margin: 0; color: #F8FAFC; }
    .header-card p { color: #94A3B8; font-size: 1.05rem; margin-top: 0.5rem; margin-bottom: 0; }
    .badge-container {
        text-align: center;
        padding: 1.2rem;
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .badge-title { font-size: 0.85rem; color: #166534; text-transform: uppercase; font-weight: 600; }
    .badge-value { font-size: 1.8rem; font-weight: 800; color: #15803D; margin-top: 0.25rem; }
    .urgent-badge {
        text-align: center;
        padding: 0.75rem;
        background: #FEF2F2;
        border: 1px solid #FCA5A5;
        color: #991B1B;
        border-radius: 8px;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .hint-text { color: #64748B; font-size: 0.85rem; margin-top: 0.75rem; }
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def ensure_log_file():
  if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=[
        "timestamp",
        "pelapor",
        "lokasi",
        "text",
        "predicted_label",
        "confidence",
        "urgency",
    ])
    df.to_csv(LOG_FILE, index=False)


def append_log(
    text: str,
    label: str,
    confidence: float,
    urgency: str,
    pelapor: str,
    lokasi: str,
):
  ensure_log_file()
  row = {
      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "pelapor": pelapor if pelapor else "Anonim",
      "lokasi": lokasi if lokasi else "Tidak Disebutkan",
      "text": text,
      "predicted_label": label,
      "confidence": f"{confidence}%",
      "urgency": urgency,
  }
  df = pd.read_csv(LOG_FILE)
  df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
  df.to_csv(LOG_FILE, index=False)


def load_logs() -> pd.DataFrame:
  ensure_log_file()
  return pd.read_csv(LOG_FILE)


def check_api_health():
  try:
    r = requests.get("https://project-skpi.onrender.com/health", timeout=3)
    return r.status_code == 200
  except Exception:
    return False


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
  st.image("logo.jpg", width=64)
  st.title("CivicReport AI")
  st.caption("Sistem Klasifikasi & Analisis Laporan Publik")
  st.divider()

  api_online = check_api_health()
  if api_online:
    st.success("🟢 API Status: Connected", icon="✅")
  else:
    st.error("🔴 API Status: Disconnected", icon="⚠️")
    st.caption("Pastikan uvicorn/FastAPI aktif di port 8000.")

  st.divider()
  st.markdown("### 📌 Fitur Utama")
  st.markdown("""
    * **NLP Classifier**: Memetakan dinas penanggung jawab.
    * **Urgency Detector**: Deteksi otomatis kasus darurat.
    * **Notification Dispatch**: Notifikasi otomatis ke unit kerja.
    * **Data Analytics**: Insight visual sebaran masalah publik.
    """)

# -----------------------------------------------------------------------------
# HEADER SECTION
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="header-card">
        <h1>🏛️ CivicReport</h1>
        <p>Pusat Kendali Laporan Masyarakat & Routing Otomatis Berbasis Kecerdasan Buatan.</p>
    </div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs([
    "📝 Klasifikasi & Dispatch",
    "📊 Dashboard & Analisis",
    "🗺️ Peta & Geospasial",
])

# -----------------------------------------------------------------------------
# TAB 1: KLASIFIKASI & DISPATCH
# -----------------------------------------------------------------------------
with tab1:
  col_input, col_result = st.columns([1.2, 0.8], gap="large")

  with col_input:
    st.subheader("Form Pelaporan Masyarakat")

    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
      pelapor_input = st.text_input(
          "Nama Pelapor (Opsional):", placeholder="Contoh: Budi Prasetyo"
      )
    with col_meta2:
      lokasi_input = st.text_input(
          "Wilayah / Kecamatan / Alamat:",
          placeholder="Contoh: Kec. Ngaliyan / RT 02 RW 05",
      )

    text_input = st.text_area(
        "Isi Keluhan Masyarakat:*",
        height=150,
        placeholder=(
            "Contoh: BAHAYA! Pipa air utama bocor deras di dekat persimpangan"
            " jalan utama, menyebabkan jalan licin dan berpotensi memicu"
            " kecelakaan..."
        ),
    )

    btn_predict = st.button(
        "🚀 Proses & Disposisi Aduan", type="primary", use_container_width=True
    )

    st.markdown(
        '<p class="hint-text">💡 <b>Tips:</b> Gunakan kata kunci seperti'
        ' <i>"darurat"</i>, <i>"bahaya"</i>, atau <i>"segera"</i> untuk'
        " mengaktifkan status prioritas tinggi.</p>",
        unsafe_allow_html=True,
    )

  with col_result:
    st.subheader("Hasil Analisis & Disposisi")

    if btn_predict:
      actual_text = text_input.strip()

      if not actual_text:
        st.warning("Silakan isi teks aduan terlebih dahulu.")
      elif not api_online:
        st.error("API FastAPI tidak aktif! Jalankan API terlebih dahulu.")
      else:
        with st.spinner("Menganalisis teks & menentukan prioritas..."):
          try:
            # === PERBAIKAN DI SINI ===
            payload = {"text": actual_text}
            resp = requests.post(API_URL, json=payload, timeout=10)
            resp.raise_for_status()
            res_json = resp.json()

            label = res_json["label"]
            confidence = res_json.get("confidence", 0.0)
            urgency = res_json.get("urgency", "🟢 NORMAL")

            # Indikator Urgensi
            st.markdown(
                f'<div class="urgent-badge">Tingkat Prioritas: {urgency}</div>',
                unsafe_allow_html=True,
            )

            # Badge Hasil & Confidence Score
            st.markdown(
                f"""
                <div class="badge-container">
                    <div class="badge-title">Unit Kerja Tujuan</div>
                    <div class="badge-value">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if confidence > 0:
              st.write(f"**Tingkat Keyakinan AI:** `{confidence}%`")
              st.progress(int(confidence) / 100)

            # Preview Notifikasi
            with st.expander(
                "📬 Preview Alert Disposisi Dinas", expanded=True
            ):
              st.caption(
                  f"Pesan otomatis terkirim ke WhatsApp / Email **Dinas"
                  f" {label}**:"
              )
              st.code(
                  f"""
[SISTEM CIVICREPORT ALERT]
Priority: {urgency}
Unit Kerja: Dinas {label}
Lokasi: {lokasi_input if lokasi_input else 'Tidak Disebutkan'}
Pelapor: {pelapor_input if pelapor_input else 'Anonim'}

Isi Aduan:
"{actual_text}"

Status: Disposisi Otomatis oleh AI
                            """,
                  language="yaml",
              )

            # Simpan ke CSV Log
            append_log(
                text=actual_text,
                label=label,
                confidence=confidence,
                urgency=urgency,
                pelapor=pelapor_input,
                lokasi=lokasi_input,
            )

          except Exception as e:
            st.error(f"Gagal memproses data: {e}")
    else:
      st.info(
          "Masukkan aduan pada form di sebelah kiri lalu klik tombol **Proses"
          " & Disposisi Aduan**."
      )

# -----------------------------------------------------------------------------
# TAB 2: DASHBOARD
# -----------------------------------------------------------------------------
with tab2:
  df = load_logs()

  if df.empty:
    st.info(
        "Belum ada data laporan yang dicatat. Cobalah melakukan klasifikasi"
        " pada Tab 'Klasifikasi & Dispatch'."
    )
  else:
    # Metrik Utama
    total_reports = len(df)
    top_label = df["predicted_label"].value_counts().idxmax()
    urgent_count = len(df[df["urgency"].str.contains("DARURAT", na=False)])

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Laporan Masuk", f"{total_reports} Laporan")
    m2.metric("Kategori Dominan", top_label)
    m3.metric("Laporan Status Darurat 🚨", f"{urgent_count} Kasus")

    st.divider()

    # Visualisasi Plotly
    col_chart1, col_chart2 = st.columns([1.2, 0.8])
    counts = df["predicted_label"].value_counts().reset_index()
    counts.columns = ["Kategori", "Jumlah"]

    with col_chart1:
      st.markdown("### Distribusi Kategori Keluhan")
      fig_bar = px.bar(
          counts,
          x="Kategori",
          y="Jumlah",
          color="Kategori",
          text="Jumlah",
          color_discrete_sequence=px.colors.qualitative.Safe,
      )
      fig_bar.update_layout(
          showlegend=False,
          margin=dict(l=10, r=10, t=20, b=10),
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
      )
      st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
      st.markdown("### Proporsi Keluhan")
      fig_pie = px.pie(
          counts,
          names="Kategori",
          values="Jumlah",
          hole=0.4,
          color_discrete_sequence=px.colors.qualitative.Safe,
      )
      fig_pie.update_layout(
          margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)"
      )
      st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # Filter & Search Log Data
    st.markdown("### 📋 Log Laporan Terbaru")

    f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
    with f_col1:
      search_query = st.text_input(
          "🔍 Cari Kata Kunci:", placeholder="Ketik lokasi / teks..."
      )
    with f_col2:
      categories = ["Semua"] + list(df["predicted_label"].unique())
      selected_cat = st.selectbox("Filter Kategori:", categories)
    with f_col3:
      csv_data = df.to_csv(index=False).encode("utf-8")
      st.markdown(
          "<div style='height: 28px;'></div>", unsafe_allow_html=True
      )
      st.download_button(
          label="📥 Export Log (CSV)",
          data=csv_data,
          file_name=f"log_keluhan_{datetime.now().strftime('%Y%m%d')}.csv",
          mime="text/csv",
          use_container_width=True,
      )

    # Apply Filters
    filtered_df = df.copy()
    if selected_cat != "Semua":
      filtered_df = filtered_df[filtered_df["predicted_label"] == selected_cat]
    if search_query:
      filtered_df = filtered_df[
          filtered_df["text"].str.contains(
              search_query, case=False, na=False
          )
          | filtered_df["lokasi"].str.contains(
              search_query, case=False, na=False
          )
      ]

    st.dataframe(
        filtered_df.sort_values(by="timestamp", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "timestamp": st.column_config.DatetimeColumn(
                "Waktu Lapor", format="DD/MM/YYYY, HH:mm"
            ),
            "pelapor": "Pelapor",
            "lokasi": "Wilayah",
            "text": "Isi Keluhan",
            "predicted_label": "Kategori AI",
            "confidence": "Akurasi",
            "urgency": "Tingkat Prioritas",
        },
    )

    # Reset Log Option
    with st.expander("⚠️ Pengaturan Administrator"):
      st.caption("Tindakan ini tidak dapat dibatalkan.")
      if st.button("Reset Log Data", type="primary"):
        df0 = pd.DataFrame(columns=[
            "timestamp",
            "pelapor",
            "lokasi",
            "text",
            "predicted_label",
            "confidence",
            "urgency",
        ])
        df0.to_csv(LOG_FILE, index=False)
        st.success("Log berhasil direset!")
        st.rerun()

# -----------------------------------------------------------------------------
# TAB 3: MAPS & GEOSPATIAL
# -----------------------------------------------------------------------------
with tab3:
  st.markdown("### 🗺️ Analisis Sebaran Laporan Wilayah")
  df_map = load_logs()

  if df_map.empty:
    st.info("Belum ada data lokasi untuk ditampilkan.")
  else:
    loc_counts = df_map["lokasi"].value_counts().reset_index()
    loc_counts.columns = ["Wilayah", "Jumlah Aduan"]

    col_m1, col_m2 = st.columns([1, 1])
    with col_m1:
      st.dataframe(loc_counts, use_container_width=True, hide_index=True)
    with col_m2:
      fig_map_bar = px.bar(
          loc_counts,
          x="Jumlah Aduan",
          y="Wilayah",
          orientation="h",
          color="Jumlah Aduan",
          color_continuous_scale="Reds",
      )
      fig_map_bar.update_layout(
          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
      )
      st.plotly_chart(fig_map_bar, use_container_width=True)
