import random
import pandas as pd

random.seed(42)

LABELS = [
    "Infrastruktur",
    "Kebersihan",
    "Banjir",
    "Keamanan",
    "Administrasi",
]

# Template per kategori (dibuat bervariasi biar tidak repetitif)
TEMPLATES = {
    "Infrastruktur": [
        "Jalan {kondisi} di {lokasi} {dampak}.",
        "Trotoar {kondisi} di {lokasi}, {dampak}.",
        "Lampu jalan {kondisi} di {lokasi} sejak {durasi}.",
        "Jembatan kecil di {lokasi} {kondisi} dan {dampak}.",
        "Marka jalan di {lokasi} {kondisi}, {dampak}.",
    ],
    "Kebersihan": [
        "Sampah {kondisi} di {lokasi} {dampak}.",
        "TPS di {lokasi} {kondisi} dan {dampak}.",
        "Selokan di {lokasi} penuh sampah, {dampak}.",
        "Bau menyengat dari tumpukan sampah di {lokasi} {dampak}.",
        "Pengangkutan sampah di {lokasi} {kondisi} sejak {durasi}.",
    ],
    "Banjir": [
        "Saat hujan {intensitas}, {lokasi} {kondisi} banjir {tinggi} cm.",
        "Drainase di {lokasi} {kondisi} sehingga banjir saat hujan {intensitas}.",
        "Air meluap dari {sumber_air} di {lokasi} {dampak}.",
        "Genangan air di {lokasi} {kondisi} sejak {durasi}.",
        "Banjir {tinggi} cm di {lokasi}, {dampak}.",
    ],
    "Keamanan": [
        "Lampu penerangan di {lokasi} {kondisi} sehingga {dampak_keamanan}.",
        "Sering terjadi {insiden} di {lokasi} pada {waktu}, mohon patroli.",
        "Area {lokasi} {kondisi} dan rawan {insiden}.",
        "Ada {insiden} dekat {lokasi}, warga merasa tidak aman.",
        "Kerumunan/parkir liar di {lokasi} {dampak_keamanan}.",
    ],
    "Administrasi": [
        "Pengurusan {dokumen} di {tempat} {kondisi} dan {dampak_admin}.",
        "Antrian {dokumen} di {tempat} {kondisi} sejak {durasi}.",
        "Proses {dokumen} di {tempat} {kondisi}, mohon perbaikan layanan.",
        "Petugas di {tempat} {kondisi} saat mengurus {dokumen}.",
        "Sistem/website layanan {tempat} {kondisi} sehingga {dampak_admin}.",
    ],
}

# Variabel kata
lokasi = [
    "RW 03", "RW 05", "depan sekolah", "dekat pasar", "jalan utama", "gang kecil",
    "sekitar puskesmas", "komplek perumahan", "jalan menuju halte", "area masjid",
    "perempatan", "dekat balai warga"
]
kondisi = [
    "berlubang", "rusak parah", "retak dan tidak rata", "ambrol", "tertutup material",
    "mati", "padam", "macet", "kotor", "menumpuk", "tidak terangkut", "penuh"
]
dampak = [
    "membahayakan pengendara", "menyebabkan kemacetan", "membuat warga kesulitan lewat",
    "mengganggu aktivitas warga", "sering menyebabkan kecelakaan kecil"
]
durasi = ["2 hari", "3 hari", "1 minggu", "2 minggu", "sebulan"]
intensitas = ["deras", "sedang", "lebat", "ekstrem"]
tinggi = ["10", "20", "30", "40", "50"]
sumber_air = ["sungai", "selokan", "drainase", "gorong-gorong"]
dampak_keamanan = [
    "rawan pencurian", "rawan kecelakaan malam", "rawan tindakan kriminal", "membuat warga khawatir"
]
insiden = ["pencurian", "begal", "balap liar", "keributan", "aksi vandalisme"]
waktu = ["malam hari", "dini hari", "sore", "akhir pekan"]
dokumen = ["KTP", "KK", "surat domisili", "akta kelahiran", "surat pindah"]
tempat = ["kelurahan", "kantor kecamatan", "loket pelayanan", "kantor desa", "mal pelayanan publik"]
dampak_admin = [
    "warga bolak-balik", "waktu tunggu terlalu lama", "informasi tidak jelas", "pengajuan tertunda"
]

def make_sentence(label: str) -> str:
    t = random.choice(TEMPLATES[label])
    return t.format(
        lokasi=random.choice(lokasi),
        kondisi=random.choice(kondisi),
        dampak=random.choice(dampak),
        durasi=random.choice(durasi),
        intensitas=random.choice(intensitas),
        tinggi=random.choice(tinggi),
        sumber_air=random.choice(sumber_air),
        dampak_keamanan=random.choice(dampak_keamanan),
        insiden=random.choice(insiden),
        waktu=random.choice(waktu),
        dokumen=random.choice(dokumen),
        tempat=random.choice(tempat),
        dampak_admin=random.choice(dampak_admin),
    )

def generate(n_per_label=120):
    rows = []
    for label in LABELS:
        for _ in range(n_per_label):
            rows.append({"text": make_sentence(label), "label": label})
    random.shuffle(rows)
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate(n_per_label=120)  # total 600 baris
    df.to_csv("data_keluhan.csv", index=False)
    print("Saved data_keluhan.csv with rows:", len(df))
    print(df.head(10))