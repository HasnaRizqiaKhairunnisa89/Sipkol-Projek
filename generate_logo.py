import matplotlib.patches as patches
import matplotlib.pyplot as plt

# Buat canvas gambar
fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
fig.patch.set_facecolor('#0F172A')  # Slate Gelap
ax.set_facecolor('#0F172A')

# Lingkaran luar (Warna Biru / Slate Enterprise)
outer_circle = plt.Circle((0.5, 0.5), 0.45, color='#1E293B', ec='#38BDF8', lw=6)
ax.add_patch(outer_circle)

# 🏛️ 1. GEDUNG PILAR (CIVIC)
# Atap Gedung
roof = patches.Polygon([[0.2, 0.62], [0.5, 0.8], [0.8, 0.62]], color='#38BDF8')
ax.add_patch(roof)
ax.add_patch(patches.Rectangle((0.22, 0.58), 0.56, 0.04, color='#93C5FD'))

# Pilar-Pilar Gedung
for x in [0.26, 0.39, 0.52, 0.65]:
  ax.add_patch(patches.Rectangle((x, 0.32), 0.09, 0.25, color='#F8FAFC'))

# Pondasi Gedung
ax.add_patch(patches.Rectangle((0.2, 0.27), 0.6, 0.05, color='#93C5FD'))

# ✦ 2. SIRKUIT / BINTANG (AI)
# Bintang AI di Pojok Atas (Kuning Emas)
star = patches.Polygon(
    [
        [0.78, 0.78],
        [0.80, 0.83],
        [0.85, 0.85],
        [0.80, 0.87],
        [0.78, 0.92],
        [0.76, 0.87],
        [0.71, 0.85],
        [0.76, 0.83],
    ],
    color='#FACC15',
)
ax.add_patch(star)

# Simbol Sirkuit Kecil
ax.plot([0.5, 0.5], [0.8, 0.88], color='#38BDF8', lw=3)
ax.plot([0.5, 0.71], [0.88, 0.88], color='#38BDF8', lw=3)
ax.add_patch(plt.Circle((0.5, 0.88), 0.015, color='#FACC15'))

# Pengaturan Tampilan Canvas
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# SIMPAN MENJADI FILE JPG
plt.savefig('logo.jpg', bbox_inches='tight', pad_inches=0, format='jpg')
print('✅ File logo.jpg berhasil dibuat dan disimpan di folder proyek Anda!')