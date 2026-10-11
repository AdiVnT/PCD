from PIL import Image
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

fig, axes = plt.subplots(1, 2, figsize=(10, 8))

axes[0].imshow(gambar, cmap="gray", vmin=0, vmax=255)
axes[0].set_title("Gambar Asli")
axes[0].axis("off")

axes[1].imshow(hasil, cmap="gray", vmin=0, vmax=255)
axes[1].set_title(f"Gambar Hasil (brightness {brightness:+d})")
axes[1].axis("off")

plt.tight_layout()
plt.show()