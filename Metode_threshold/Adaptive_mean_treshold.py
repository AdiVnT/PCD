
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

# 3. Menyiapkan gambar hasil
hasil = np.zeros((tinggi, lebar), dtype=np.uint8)

# 4. Perulangan setiap piksel
for y in range(tinggi):
    for x in range(lebar):

        # Menentukan batas area lokal
        y1 = max(0, y - jarak)
        y2 = min(tinggi, y + jarak + 1)
        x1 = max(0, x - jarak)
        x2 = min(lebar, x + jarak + 1)

        # Mengambil area piksel tetangga
        area = img[y1:y2, x1:x2]

        # Menghitung rata-rata lokal
        mean = np.mean(area)

        # Menghitung threshold lokal
        threshold = mean - C

        # Membandingkan piksel dengan threshold
        if img[y, x] > threshold:
            hasil[y, x] = 255
        else:
            hasil[y, x] = 0

# 5. Menampilkan hasil
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray")
plt.title("Gambar Grayscale")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(hasil, cmap="gray")
plt.title("Adaptive Mean Manual")
plt.axis("off")

plt.tight_layout()
plt.show()
