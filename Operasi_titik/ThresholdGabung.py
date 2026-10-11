
import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("Citrainputgrey.jpg", cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Gambar tidak ditemukan.")
    raise SystemExit

# BATAS THRESHOLD
try:
    threshold = int(input("Masukkan threshold tunggal (0-255): "))
    lower = int(input("Masukkan batas bawah threshold ganda (0-255): "))
    upper = int(input("Masukkan batas atas threshold ganda (0-255): "))
except ValueError:
    print("Batas harus berupa bilangan bulat.")
    raise SystemExit

if not all(0 <= value <= 255 for value in (threshold, lower, upper)):
    print("Semua batas harus berada di antara 0 dan 255.")
    raise SystemExit

if lower > upper:
    print("Batas bawah tidak boleh lebih besar dari batas atas.")
    raise SystemExit

# OUTPUT
height, width = image.shape

output_tunggal = np.zeros((height, width), dtype=np.uint8)
output_ganda = np.zeros((height, width), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        pixel = image[y, x]

        # Threshold tunggal
        if pixel < threshold:
            output_tunggal[y, x] = 0
        else:
            output_tunggal[y, x] = 1

        # Threshold ganda
        if lower <= pixel <= upper:
            output_ganda[y, x] = 1
        else:
            output_ganda[y, x] = 0

# UBAH NILAI BINER MENJADI 0 DAN 255
hasil_tunggal = output_tunggal * 255
hasil_ganda = output_ganda * 255

cv2.imwrite("hasil_threshold_tunggal.png", hasil_tunggal)
cv2.imwrite("hasil_threshold_ganda.png", hasil_ganda)

print("Hasil threshold berhasil disimpan.")
print("Threshold Tunggal:")
print(np.unique(hasil_tunggal, return_counts=True))

print("Threshold Ganda:")
print(np.unique(hasil_ganda, return_counts=True))

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

axes[0, 0].imshow(image, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Gambar Asli")
axes[0, 0].axis("off")

axes[0, 1].imshow(hasil_tunggal, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title(f"Threshold Tunggal (T={threshold})")
axes[0, 1].axis("off")

axes[0, 2].imshow(hasil_ganda, cmap="gray", vmin=0, vmax=255)
axes[0, 2].set_title(f"Threshold Ganda ({lower}-{upper})")
axes[0, 2].axis("off")

# Histogram gambar asli
axes[1, 0].hist(image.ravel(), bins=256, range=(0, 256))
axes[1, 0].set_title("Histogram Gambar Asli")
axes[1, 0].set_xlabel("Nilai Intensitas")
axes[1, 0].set_ylabel("Jumlah Piksel")
axes[1, 0].set_xlim(0, 256)

# Histogram threshold tunggal
jumlah_hitam_tunggal = np.count_nonzero(hasil_tunggal == 0)
jumlah_putih_tunggal = np.count_nonzero(hasil_tunggal == 255)

axes[1, 1].bar(
    [0, 255],
    [jumlah_hitam_tunggal, jumlah_putih_tunggal],
    width=3
)
axes[1, 1].set_title("Histogram Threshold Tunggal")
axes[1, 1].set_xlabel("Nilai Intensitas")
axes[1, 1].set_ylabel("Jumlah Piksel")
axes[1, 1].set_xlim(-5, 260)
axes[1, 1].set_xticks([0, 50, 100, 150, 200, 255])

# Histogram threshold ganda
jumlah_hitam_ganda = np.count_nonzero(hasil_ganda == 0)
jumlah_putih_ganda = np.count_nonzero(hasil_ganda == 255)

axes[1, 2].bar(
    [0, 255],
    [jumlah_hitam_ganda, jumlah_putih_ganda],
    width=3
)
axes[1, 2].set_title("Histogram Threshold Ganda")
axes[1, 2].set_xlabel("Nilai Intensitas")
axes[1, 2].set_ylabel("Jumlah Piksel")
axes[1, 2].set_xlim(-5, 260)
axes[1, 2].set_xticks([0, 50, 100, 150, 200, 255])


plt.tight_layout()
plt.show()