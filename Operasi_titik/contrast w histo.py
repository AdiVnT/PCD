from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

gambar = Image.open("Citrainputgrey.jpg")

gambar = gambar.convert("L")

contrast = float(input("Contrast (misal 0.1 - 3.0, 1.0 = tidak berubah): "))

hasil = Image.new("L", gambar.size)

for y in range(gambar.height):
    for x in range(gambar.width):
        nilai = gambar.getpixel((x, y))
        nilai_baru = (nilai - 128) * contrast + 128

        nilai_baru = max(0, min(255, int(nilai_baru)))

        hasil.putpixel((x, y), nilai_baru)

hasil.save(r"D:\hasil_contrast.png")

print("Contrast berhasil diubah.")
print("Nilai contrast    :", contrast)
print("Resolusi          :", hasil.size)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].imshow(gambar, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Gambar Asli")
axes[0, 0].axis("off")

axes[0, 1].imshow(hasil, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title(f"Gambar Hasil (contrast {contrast})")
axes[0, 1].axis("off")

axes[1, 0].hist(np.array(gambar).ravel(), bins=256, range=(0, 256))
axes[1, 0].set_title("Histogram Gambar Asli")
axes[1, 0].set_xlabel("Nilai Intensitas")
axes[1, 0].set_ylabel("Jumlah Piksel")
axes[1, 0].set_xlim([0, 256])
 
axes[1, 1].hist(np.array(hasil).ravel(), bins=256, range=(0, 256))
axes[1, 1].set_title("Histogram Gambar Hasil")
axes[1, 1].set_xlabel("Nilai Intensitas")
axes[1, 1].set_ylabel("Jumlah Piksel")
axes[1, 1].set_xlim([0, 256])

plt.tight_layout()
plt.show()