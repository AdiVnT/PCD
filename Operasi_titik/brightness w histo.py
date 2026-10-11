from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

gambar = Image.open("Citrainputgrey.jpg")

gambar = gambar.convert("L")

brightness = int(input("Brightness (-255 sampai 255): "))

hasil = Image.new("L", gambar.size)

for y in range(gambar.height):
    for x in range(gambar.width):
        nilai = gambar.getpixel((x, y))
        nilai_baru = nilai + brightness

        nilai_baru = max(0, min(255, nilai_baru))

        hasil.putpixel((x, y), nilai_baru)

hasil.save(r"D:\hasil_brightness2.png")

print("Brightness berhasil diubah.")
print("Nilai brightness  :", brightness)
print("Resolusi          :", hasil.size)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Gambar asli
axes[0, 0].imshow(gambar, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Gambar Asli")
axes[0, 0].axis("off")

# Gambar hasil
axes[0, 1].imshow(hasil, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title(f"Gambar Hasil (brightness {brightness:+d})")
axes[0, 1].axis("off")

# Histogram gambar asli
axes[1, 0].hist(np.array(gambar).ravel(), bins=256, range=(0, 256))
axes[1, 0].set_title("Histogram Gambar Asli")
axes[1, 0].set_xlabel("Nilai Intensitas")
axes[1, 0].set_ylabel("Jumlah Piksel")
axes[1, 0].set_xlim([0, 256])

# Histogram gambar hasil
axes[1, 1].hist(np.array(hasil).ravel(), bins=256, range=(0, 256))
axes[1, 1].set_title("Histogram Gambar Hasil")
axes[1, 1].set_xlabel("Nilai Intensitas")
axes[1, 1].set_ylabel("Jumlah Piksel")
axes[1, 1].set_xlim([0, 256])

plt.tight_layout()
plt.show()