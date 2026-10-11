
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("image.png")

if img is None:
    print("Gambar tidak ditemukan!")
    exit()

# Konversi BGR ke RGB agar warna tampil benar di Matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Ambil setiap channel
B = img[:, :, 0].astype(np.float32)
G = img[:, :, 1].astype(np.float32)
R = img[:, :, 2].astype(np.float32)

# METODE 1: Rata-rata
gray_rata_rata = (R + G + B) / 3.0
gray_rata_rata = gray_rata_rata.astype(np.uint8)

# METODE 2: Pembobotan NTSC
gray_ntsc = (
    0.299 * R +
    0.587 * G +
    0.114 * B
).astype(np.uint8)

cv2.imwrite("grayscale_rata_rata.png", gray_rata_rata)
cv2.imwrite("grayscale_ntsc.png", gray_ntsc)

print("Konversi grayscale berhasil disimpan.")

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# Gambar asli
axes[0, 0].imshow(img_rgb)
axes[0, 0].set_title("Gambar Asli")
axes[0, 0].axis("off")

# Hasil metode rata-rata
axes[0, 1].imshow(gray_rata_rata, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title("Grayscale Metode Rata-rata")
axes[0, 1].axis("off")

# Hasil metode NTSC
axes[0, 2].imshow(gray_ntsc, cmap="gray", vmin=0, vmax=255)
axes[0, 2].set_title("Grayscale Metode NTSC")
axes[0, 2].axis("off")

# Histogram gambar asli (RGB)
axes[1, 0].hist(
    img[:, :, 2].ravel(), bins=256, range=(0, 256),
    color="red", histtype="step", linewidth=1.5, label="Red"
)

axes[1, 0].hist(
    img[:, :, 1].ravel(), bins=256, range=(0, 256),
    color="green", histtype="step", linewidth=1.5, label="Green"
)

axes[1, 0].hist(
    img[:, :, 0].ravel(), bins=256, range=(0, 256),
    color="blue", histtype="step", linewidth=1.5, label="Blue"
)

axes[1, 0].set_title("Histogram Gambar Asli (RGB)")
axes[1, 0].set_xlabel("Nilai Intensitas")
axes[1, 0].set_ylabel("Jumlah Piksel")
axes[1, 0].set_xlim(0, 256)
axes[1, 0].legend()

# Histogram hasil metode rata-rata
axes[1, 1].hist(gray_rata_rata.ravel(), bins=256, range=(0, 256))
axes[1, 1].set_title("Histogram Grayscale Rata-rata")
axes[1, 1].set_xlabel("Nilai Intensitas")
axes[1, 1].set_ylabel("Jumlah Piksel")
axes[1, 1].set_xlim(0, 256)

# Histogram hasil metode NTSC
axes[1, 2].hist(gray_ntsc.ravel(), bins=256, range=(0, 256))
axes[1, 2].set_title("Histogram Grayscale NTSC")
axes[1, 2].set_xlabel("Nilai Intensitas")
axes[1, 2].set_ylabel("Jumlah Piksel")
axes[1, 2].set_xlim(0, 256)

plt.tight_layout()
plt.show()