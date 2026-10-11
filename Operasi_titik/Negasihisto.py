import cv2
import matplotlib.pyplot as plt

gambar = cv2.imread("Citrainputgrey.jpg", cv2.IMREAD_GRAYSCALE)

if gambar is None:
    print("Gambar tidak ditemukan!")
    exit()

# Proses negasi
negasi = 255 - gambar

cv2.imwrite("CitraNegasi.jpg", negasi)

# perhitungan 3 piksel awal

print("\n=== PERHITUNGAN 3 PIXEL AWAL ===")

for i in range(3):
    x = i
    y = 0

    nilai_asli = gambar[y, x]
    nilai_negasi = 255 - nilai_asli

    print(f"Pixel {i + 1}")
    print(f"Koordinat (x, y) : ({x}, {y})")
    print(f"Nilai asli      : {nilai_asli}")
    print(f"Rumus negasi    : 255 - {nilai_asli}")
    print(f"Hasil negasi    : {nilai_negasi}")
    print()


fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Gambar asli
axes[0, 0].imshow(gambar, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Gambar Asli")
axes[0, 0].axis("off")

# Histogram gambar asli
axes[0, 1].hist(gambar.ravel(), bins=256, range=(0, 256))
axes[0, 1].set_title("Histogram Gambar Asli")
axes[0, 1].set_xlabel("Nilai Intensitas")
axes[0, 1].set_ylabel("Jumlah Piksel")
axes[0, 1].set_xlim([0, 256])

# Gambar negasi
axes[1, 0].imshow(negasi, cmap="gray", vmin=0, vmax=255)
axes[1, 0].set_title("Gambar Negasi")
axes[1, 0].axis("off")

# Histogram gambar negasi
axes[1, 1].hist(negasi.ravel(), bins=256, range=(0, 256))
axes[1, 1].set_title("Histogram Gambar Negasi")
axes[1, 1].set_xlabel("Nilai Intensitas")
axes[1, 1].set_ylabel("Jumlah Piksel")
axes[1, 1].set_xlim([0, 256])

plt.tight_layout()
plt.show()
