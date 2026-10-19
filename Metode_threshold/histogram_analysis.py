import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = r"D:\KULIAH\Akademis\Sem 3\PCD\PCD\Citra\citra_rgb.png"

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

image_original = cv2.imread(image_path, cv2.IMREAD_COLOR)
if image is None:
    print("Gambar tidak ditemukan. Periksa kembali lokasi file.")
    raise SystemExit

image_rgb = cv2.cvtColor(image_original, cv2.COLOR_BGR2RGB)

tinggi, lebar = image.shape
total_piksel = tinggi * lebar

# MENGHITUNG HISTOGRAM
histogram = [0] * 256

for y in range(tinggi):
    for x in range(lebar):
        intensitas = image[y, x]
        histogram[intensitas] += 1

# MENGHITUNG CDF
cdf = [0.0] * 256
kumulatif = 0

for i in range(256):
    kumulatif += histogram[i]
    cdf[i] = kumulatif / total_piksel

# METODE 1: CDF > 0.5
threshold_cdf = 0

for i in range(256):
    if cdf[i] > 0.5:
        threshold_cdf = i
        break

# Terapkan thresholding CDF
hasil_cdf = np.zeros_like(image)

for y in range(tinggi):
    for x in range(lebar):
        if image[y, x] > threshold_cdf:
            hasil_cdf[y, x] = 255
        else:
            hasil_cdf[y, x] = 0

# METODE 2: VALLEY DETECTION

# Menghaluskan histogram dengan moving average
hist_halus = [0.0] * 256
ukuran_jendela = 11
radius = ukuran_jendela // 2

for i in range(256):
    awal = max(0, i - radius)
    akhir = min(255, i + radius)

    jumlah = 0
    banyak = 0

    for j in range(awal, akhir + 1):
        jumlah += histogram[j]
        banyak += 1

    hist_halus[i] = jumlah / banyak

# Mencari puncak
kandidat_puncak = []
radius_prominence = ukuran_jendela * 3

for i in range(1, 255):
    if hist_halus[i] >= hist_halus[i - 1] and hist_halus[i] > hist_halus[i + 1]:
        awal_kiri = max(0, i - radius_prominence)
        awal_kanan = min(255, i + radius_prominence)

        lembah_kiri = min(hist_halus[awal_kiri:i + 1])
        lembah_kanan = min(hist_halus[i:awal_kanan + 1])
        prominence = hist_halus[i] - max(lembah_kiri, lembah_kanan)

        kandidat_puncak.append((i, prominence))

# Pilih dua puncak paling menonjol yang cukup berjauhan
kandidat_puncak.sort(key=lambda item: item[1], reverse=True)
jarak_minimum = ukuran_jendela * 3
puncak_terpilih = []

for posisi, prominence in kandidat_puncak:
    if all(abs(posisi - p) >= jarak_minimum for p in puncak_terpilih):
        puncak_terpilih.append(posisi)

    if len(puncak_terpilih) == 2:
        break

if len(puncak_terpilih) < 2:
    raise ValueError(
        "Tidak ditemukan dua puncak histogram yang cukup terpisah. "
        "Coba ubah ukuran_jendela atau periksa histogram citra."
    )

puncak1, puncak2 = sorted(puncak_terpilih)

# Mencari lembah di antara kedua puncak
threshold_valley = puncak1

for i in range(puncak1 + 1, puncak2 + 1):
    if hist_halus[i] < hist_halus[threshold_valley]:
        threshold_valley = i

# Terapkan thresholding Valley
hasil_valley = np.zeros_like(image)

for y in range(tinggi):
    for x in range(lebar):
        if image[y, x] > threshold_valley:
            hasil_valley[y, x] = 255
        else:
            hasil_valley[y, x] = 0

# MENAMPILKAN NILAI
print("Total piksel:", total_piksel)
print("Total piksel yang dihitung histogram:", sum(histogram))
print()
print("METODE 1 - CDF")
print("Threshold CDF:", threshold_cdf)
print()
print("METODE 2 - VALLEY DETECTION")
print("Puncak pertama otomatis:", puncak1)
print("Puncak kedua otomatis:", puncak2)
print("Threshold Valley:", threshold_valley)

# VISUALISASI
fig = plt.figure(
    "Histogram Analysis - CDF dan Valley Detection",
    figsize=(18, 11),
    dpi=100
)
gs = fig.add_gridspec(
    3, 1,
    height_ratios=[0.35, 1.8, 1.8],
    hspace=0.28
)

# CITRA ASLI
original_gs = gs[0].subgridspec(1, 3, wspace=0)
ax_original = fig.add_subplot(original_gs[0, 1])
ax_original.imshow(image_rgb)
ax_original.set_title("Citra Asli Berwarna", fontsize=10, pad=2)
ax_original.axis("off")


# METODE CDF
cdf_gs = gs[1].subgridspec(1, 4, wspace=0.32)

ax1 = fig.add_subplot(cdf_gs[0, 0])
ax1.imshow(image, cmap="gray", vmin=0, vmax=255)
ax1.set_title("Citra Grayscale - CDF")
ax1.axis("off")

ax2 = fig.add_subplot(cdf_gs[0, 1])
ax2.bar(range(256), histogram, width=1)
ax2.axvline(
    threshold_cdf, linestyle="--",
    label=f"Threshold = {threshold_cdf}"
)
ax2.set_title("Histogram Intensitas")
ax2.set_xlabel("Intensitas Piksel")
ax2.set_ylabel("Jumlah Piksel")
ax2.legend(fontsize=8)

ax3 = fig.add_subplot(cdf_gs[0, 2])
ax3.plot(range(256), cdf, label="CDF")
ax3.axhline(0.5, linestyle="--", label="CDF = 0.5")
ax3.axvline(
    threshold_cdf, linestyle="--",
    label=f"Threshold = {threshold_cdf}"
)
ax3.set_title("Cumulative Distribution Function")
ax3.set_xlabel("Intensitas Piksel")
ax3.set_ylabel("CDF")
ax3.legend(fontsize=8)

ax4 = fig.add_subplot(cdf_gs[0, 3])
ax4.imshow(hasil_cdf, cmap="gray", vmin=0, vmax=255)
ax4.set_title(f"Hasil Thresholding CDF (T = {threshold_cdf})")
ax4.axis("off")

# METODE VALLEY DETECTION
valley_gs = gs[2].subgridspec(1, 4, wspace=0.32)

ax5 = fig.add_subplot(valley_gs[0, 0])
ax5.imshow(image, cmap="gray", vmin=0, vmax=255)
ax5.set_title("Citra Grayscale - Valley")
ax5.axis("off")

ax6 = fig.add_subplot(valley_gs[0, 1:3])
ax6.bar(
    range(256), histogram, width=1, alpha=0.4,
    label="Histogram Asli"
)
ax6.plot(range(256), hist_halus, label="Histogram Halus")
ax6.axvline(puncak1, linestyle=":", label=f"Puncak 1 = {puncak1}")
ax6.axvline(puncak2, linestyle=":", label=f"Puncak 2 = {puncak2}")
ax6.axvline(
    threshold_valley, linestyle="--",
    label=f"Threshold Valley = {threshold_valley}"
)
ax6.set_title("Histogram dan Valley Detection")
ax6.set_xlabel("Intensitas Piksel")
ax6.set_ylabel("Jumlah Piksel")
ax6.legend(fontsize=8)

ax7 = fig.add_subplot(valley_gs[0, 3])
ax7.imshow(hasil_valley, cmap="gray", vmin=0, vmax=255)
ax7.set_title(f"Hasil Thresholding Valley (T = {threshold_valley})")
ax7.axis("off")

fig.subplots_adjust(top=0.97, bottom=0.06, left=0.045, right=0.985)
plt.show()