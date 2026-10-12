import cv2
import numpy as np
import matplotlib.pyplot as plt

# Baca citra grayscale
image = cv2.imread("noise_gaussian.png", cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Gambar tidak ditemukan.")
    exit()

height, width = image.shape

# Padding 1 piksel untuk window 3x3
padded = np.pad(image, 1, mode="edge")

# Kernel Gaussian 3x3
kernel = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
], dtype=np.float32)

# Citra hasil
output = np.zeros((height, width), dtype=np.uint8)

# Proses setiap piksel
for y in range(height):
    for x in range(width):

        # Ambil window 3x3
        window = padded[y:y+3, x:x+3].astype(np.float32)

        # Perkalian window dengan kernel
        hasil_perkalian = window * kernel

        # Jumlahkan dan bagi dengan total bobot = 16
        gaussian_value = np.sum(hasil_perkalian) / 16

        # Simpan hasil
        output[y, x] = np.clip(gaussian_value, 0, 255)

# Simpan hasil
cv2.imwrite("hasil_gaussian.jpg", output)

# Tampilkan
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].imshow(image, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Citra Asli")
axes[0, 0].axis("off")

axes[0, 1].imshow(output, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title("Gaussian Filter")
axes[0, 1].axis("off")

axes[1, 0].hist(image.ravel(), bins=256, range=(0, 256), color="blue")
axes[1, 0].set_title("Histogram Citra Asli")
axes[1, 0].set_xlabel("Intensitas Piksel")
axes[1, 0].set_ylabel("Frekuensi")
axes[1, 0].set_xlim(0, 255)

axes[1, 1].hist(output.ravel(), bins=256, range=(0, 256), color="green")
axes[1, 1].set_title("Histogram Gaussian Filter")
axes[1, 1].set_xlabel("Intensitas Piksel")
axes[1, 1].set_ylabel("Frekuensi")
axes[1, 1].set_xlim(0, 255)

plt.tight_layout()
plt.show()