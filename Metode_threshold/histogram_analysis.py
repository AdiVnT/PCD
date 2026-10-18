import cv2
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 1. MEMBACA CITRA GRAYSCALE
# ==============================
image = cv2.imread(r"D:\KULIAH\Akademis\Sem 3\PCD\PCD\Citra\citra_rgb.png", cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Gambar tidak ditemukan.")
    exit()

tinggi, lebar = image.shape
total_piksel = tinggi * lebar

# ==============================
# 2. MENGHITUNG HISTOGRAM MANUAL
# ==============================
histogram = [0] * 256

for y in range(tinggi):
    for x in range(lebar):
        intensitas = image[y, x]
        histogram[intensitas] += 1

# ==============================
# 3. MENGHITUNG CDF MANUAL
# ==============================
cdf = [0.0] * 256
kumulatif = 0

for i in range(256):
    kumulatif += histogram[i]
    cdf[i] = kumulatif / total_piksel

# ==============================
# METODE 1: CDF > 0.5
# ==============================
threshold_cdf = 0

for i in range(256):
    if cdf[i] > 0.5:
        threshold_cdf = i
        break

# ==============================
# METODE 2: VALLEY DETECTION
# ==============================

# A. Menghaluskan histogram dengan moving average
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

# B. Mencari dua puncak histogram
# Rentang dipilih berdasarkan histogram citra burungmu.
# Puncak pertama: intensitas 80-129
# Puncak kedua: intensitas 150-209

puncak1 = 80

for i in range(81, 130):
    if hist_halus[i] > hist_halus[puncak1]:
        puncak1 = i

puncak2 = 150

for i in range(151, 210):
    if hist_halus[i] > hist_halus[puncak2]:
        puncak2 = i

# C. Mencari lembah di antara kedua puncak
kiri = min(puncak1, puncak2)
kanan = max(puncak1, puncak2)

threshold_valley = kiri

for i in range(kiri + 1, kanan + 1):
    if hist_halus[i] < hist_halus[threshold_valley]:
        threshold_valley = i

# ==============================
# 4. THRESHOLDING KEDUA METODE
# ==============================
hasil_cdf = np.zeros_like(image)
hasil_valley = np.zeros_like(image)
perbedaan = np.zeros_like(image)

jumlah_berbeda = 0

for y in range(tinggi):
    for x in range(lebar):
        piksel = image[y, x]

        # Metode CDF
        if piksel > threshold_cdf:
            hasil_cdf[y, x] = 255
        else:
            hasil_cdf[y, x] = 0

        # Metode Valley
        if piksel > threshold_valley:
            hasil_valley[y, x] = 255
        else:
            hasil_valley[y, x] = 0

        # Perbedaan hasil kedua metode
        if hasil_cdf[y, x] != hasil_valley[y, x]:
            perbedaan[y, x] = 255
            jumlah_berbeda += 1

# ==============================
# 5. MENAMPILKAN NILAI
# ==============================
print("Total piksel:", total_piksel)
print("Total histogram:", sum(histogram))
print()
print("METODE 1 - CDF")
print("Threshold CDF:", threshold_cdf)
print()
print("METODE 2 - VALLEY DETECTION")
print("Puncak pertama:", puncak1)
print("Puncak kedua:", puncak2)
print("Threshold Valley:", threshold_valley)
print()
print("Jumlah piksel berbeda:", jumlah_berbeda)
print("Persentase perbedaan:",
      round(jumlah_berbeda / total_piksel * 100, 2), "%")

# ==============================
# 6. VISUALISASI PERBANDINGAN
# ==============================
plt.figure(figsize=(16, 9))

# Citra grayscale
plt.subplot(2, 3, 1)
plt.imshow(image, cmap="gray", vmin=0, vmax=255)
plt.title("Citra Grayscale")
plt.axis("off")

# Histogram dan threshold
plt.subplot(2, 3, 2)
plt.bar(range(256), histogram, width=1, alpha=0.4,
        label="Histogram")
plt.plot(range(256), hist_halus, label="Histogram Halus")

plt.axvline(puncak1, linestyle=":", label=f"Puncak 1 = {puncak1}")
plt.axvline(puncak2, linestyle=":", label=f"Puncak 2 = {puncak2}")
plt.axvline(threshold_cdf, linestyle="--",
            label=f"CDF = {threshold_cdf}")
plt.axvline(threshold_valley, linestyle="-.",
            label=f"Valley = {threshold_valley}")

plt.title("Perbandingan Histogram")
plt.xlabel("Intensitas Piksel")
plt.ylabel("Jumlah Piksel")
plt.legend(fontsize=8)

# Grafik CDF
plt.subplot(2, 3, 3)
plt.plot(range(256), cdf, label="CDF")
plt.axhline(0.5, linestyle="--", label="CDF = 0.5")
plt.axvline(threshold_cdf, linestyle="--",
            label=f"T CDF = {threshold_cdf}")
plt.axvline(threshold_valley, linestyle="-.",
            label=f"T Valley = {threshold_valley}")

plt.title("Cumulative Distribution Function")
plt.xlabel("Intensitas Piksel")
plt.ylabel("CDF")
plt.legend(fontsize=8)

# Hasil metode CDF
plt.subplot(2, 3, 4)
plt.imshow(hasil_cdf, cmap="gray", vmin=0, vmax=255)
plt.title(f"Hasil CDF (T = {threshold_cdf})")
plt.axis("off")

# Hasil metode Valley
plt.subplot(2, 3, 5)
plt.imshow(hasil_valley, cmap="gray", vmin=0, vmax=255)
plt.title(f"Hasil Valley (T = {threshold_valley})")
plt.axis("off")

# Piksel yang berbeda
plt.subplot(2, 3, 6)
plt.imshow(perbedaan, cmap="gray", vmin=0, vmax=255)
plt.title("Perbedaan Kedua Hasil")
plt.axis("off")

plt.tight_layout()
plt.show()