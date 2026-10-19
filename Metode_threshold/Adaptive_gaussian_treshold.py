
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 1. Membaca gambar grayscale
gambar = Image.open("gambar.jpg").convert("L")
img = np.array(gambar)

tinggi, lebar = img.shape

# 2. Menentukan parameter
block_size = 11
C = 2
jarak = block_size // 2

# 3. Membuat kernel Gaussian
kernel = np.zeros((block_size, block_size), dtype=float)
sigma = block_size / 6

for i in range(block_size):
    for j in range(block_size):
        x = i - jarak
        y = j - jarak

        kernel[i, j] = np.exp(
            -(x**2 + y**2) / (2 * sigma**2)
        )

# Normalisasi bobot agar jumlahnya 1
kernel = kernel / np.sum(kernel)

# 4. Menyiapkan gambar hasil
hasil = np.zeros((tinggi, lebar), dtype=np.uint8)

# 5. Perulangan setiap piksel
for y in range(tinggi):
    for x in range(lebar):

        # Menentukan batas area lokal
        y1 = max(0, y - jarak)
        y2 = min(tinggi, y + jarak + 1)
        x1 = max(0, x - jarak)
        x2 = min(lebar, x + jarak + 1)

        # Mengambil area tetangga
        area = img[y1:y2, x1:x2]

        # Mengambil bobot kernel yang sesuai
        bobot = kernel[
            y1 - (y - jarak):y2 - (y - jarak),
            x1 - (x - jarak):x2 - (x - jarak)
        ]

        # Menghitung rata-rata berbobot Gaussian
        mean_gaussian = np.sum(area * bobot) / np.sum(bobot)

        # Menghitung threshold lokal
        threshold = mean_gaussian - C

        # Mengubah piksel menjadi hitam atau putih
        if img[y, x] > threshold:
            hasil[y, x] = 255
        else:
            hasil[y, x] = 0

# 6. Menampilkan gambar
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray")
plt.title("Grayscale")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(hasil, cmap="gray")
plt.title("Adaptive Gaussian Manual")
plt.axis("off")

plt.tight_layout()
plt.show()
