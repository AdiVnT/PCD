import cv2
import numpy as np
import matplotlib.pyplot as plt

# Baca citra grayscale
image = cv2.imread("emboss3.png", cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Gambar tidak ditemukan.")
    exit()

# Input derajat emboss
try:
    beta = int(input("Masukkan derajat emboss (beta): "))
except ValueError:
    print("Beta harus berupa bilangan bulat.")
    exit()

height, width = image.shape

# Padding 1 piksel agar bagian tepi tetap dapat diproses
padded = np.pad(image, 1, mode="edge")

# Membuat citra hasil
output_kiri = np.zeros((height, width), dtype=np.uint8)
output_kanan_atas = np.zeros((height, width), dtype=np.uint8)

# Membuat mask emboss
mask_kiri = np.array([
    [-beta, 0, beta],
    [-beta, 1, beta],
    [-beta, 0, beta]
])

mask_kanan_atas = np.array([
    [0, -beta, -beta],
    [beta, 1, -beta],
    [beta, beta, 0]
])

# Proses setiap piksel
for y in range(height):
    for x in range(width):

        # Ambil window 3x3
        window = padded[y:y+3, x:x+3].astype(np.float32)

        # Emboss arah kiri
        hasil_kiri = np.sum(window * mask_kiri)
        output_kiri[y, x] = np.clip(hasil_kiri, 0, 255)

        # Emboss arah kanan atas
        hasil_kanan_atas = np.sum(window * mask_kanan_atas)
        output_kanan_atas[y, x] = np.clip(hasil_kanan_atas, 0, 255)

# Simpan hasil
cv2.imwrite("hasil_emboss_kiri.jpg", output_kiri)
cv2.imwrite("hasil_emboss_kanan_atas.jpg", output_kanan_atas)

# Tampilkan hasil
fig, axes = plt.subplots(1, 3, figsize=(12, 5))

axes[0].imshow(image, cmap="gray", vmin=0, vmax=255)
axes[0].set_title("Citra Asli")
axes[0].axis("off")

axes[1].imshow(output_kiri, cmap="gray", vmin=0, vmax=255)
axes[1].set_title(f"Emboss Arah Kiri (β={beta})")
axes[1].axis("off")

axes[2].imshow(output_kanan_atas, cmap="gray", vmin=0, vmax=255)
axes[2].set_title(f"Emboss Arah Kanan Atas (β={beta})")
axes[2].axis("off")

plt.tight_layout()
plt.show()