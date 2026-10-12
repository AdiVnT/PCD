from PIL import Image
import numpy as np

# Membaca gambar dan mengubah menjadi grayscale
img_asli = Image.open(
    r"C:\Users\adi\Documents\SMT3\pcd\Screenshot 2026-10-04 222533.png"
).convert("L")

# Menampilkan ukuran gambar
lebar, tinggi = img_asli.size

print("Ukuran gambar:", lebar, "x", tinggi)

# Membuat gambar hasil
hasil = Image.new("L", (lebar, tinggi))

# Mask Roberts pertama
mask_1 = [
    [1, 0],
    [0, -1]
]

# Mask Roberts kedua
mask_2 = [
    [0, 1],
    [-1, 0]
]

# Proses deteksi tepi secara manual
for y in range(tinggi - 1):
    for x in range(lebar - 1):

        # Mengambil nilai piksel untuk mask 1
        p00 = img_asli.getpixel((x, y))
        p01 = img_asli.getpixel((x + 1, y))
        p10 = img_asli.getpixel((x, y + 1))
        p11 = img_asli.getpixel((x + 1, y + 1))

        # Perhitungan mask Roberts pertama
        K1 = (
            p00 * mask_1[0][0] +
            p01 * mask_1[0][1] +
            p10 * mask_1[1][0] +
            p11 * mask_1[1][1]
        )

        # Perhitungan mask Roberts kedua
        K2 = (
            p00 * mask_2[0][0] +
            p01 * mask_2[0][1] +
            p10 * mask_2[1][0] +
            p11 * mask_2[1][1]
        )

        # Mengambil nilai absolut
        K1 = abs(K1)
        K2 = abs(K2)

        # Menggabungkan kedua hasil
        # Rumus:
        # K0(x,y) = max(|K1(x,y)|, |K2(x,y)|)
        K0 = max(K1, K2)

        # Membatasi nilai agar berada pada 0-255
        K0 = min(255, K0)

        # Menyimpan hasil
        hasil.putpixel((x, y), K0)

# Menampilkan gambar asli dan hasil
img_asli.show()
hasil.show()

# Menyimpan hasil
hasil.save("hasil_roberts.jpg")

print("Deteksi tepi Roberts selesai!")
print("Hasil disimpan sebagai hasil_roberts.jpg")