from PIL import Image

# Membaca gambar dan mengubah menjadi grayscale
img_asli = Image.open(
    r"C:\Users\adi\Documents\SMT3\pcd\Screenshot 2026-10-04 222533.png"
).convert("L")

# Menampilkan ukuran gambar
lebar, tinggi = img_asli.size

print("Ukuran gambar:", lebar, "x", tinggi)

# Membuat gambar kosong untuk hasil
hasil = Image.new("L", (lebar, tinggi))

# Mask Isotropik Horizontal
mask = [
    [-1, -1.414, -1],
    [ 0,  0,     0],
    [ 1,  1.414, 1]
]

# Proses deteksi tepi secara manual
for y in range(1, tinggi - 1):
    for x in range(1, lebar - 1):

        # Mengambil 9 piksel di sekitar titik
        p00 = img_asli.getpixel((x - 1, y - 1))
        p01 = img_asli.getpixel((x,     y - 1))
        p02 = img_asli.getpixel((x + 1, y - 1))

        p10 = img_asli.getpixel((x - 1, y))
        p11 = img_asli.getpixel((x,     y))
        p12 = img_asli.getpixel((x + 1, y))

        p20 = img_asli.getpixel((x - 1, y + 1))
        p21 = img_asli.getpixel((x,     y + 1))
        p22 = img_asli.getpixel((x + 1, y + 1))

        # Perhitungan konvolusi Isotropik
        nilai = (
            p00 * mask[0][0] +
            p01 * mask[0][1] +
            p02 * mask[0][2] +
            p10 * mask[1][0] +
            p11 * mask[1][1] +
            p12 * mask[1][2] +
            p20 * mask[2][0] +
            p21 * mask[2][1] +
            p22 * mask[2][2]
        )

        # Nilai absolut
        nilai = abs(nilai)

        # Membatasi nilai 0-255
        nilai = min(255, int(nilai))

        # Menyimpan hasil
        hasil.putpixel((x, y), nilai)

# Menampilkan gambar asli dan hasil
img_asli.show()
hasil.show()

# Menyimpan hasil
hasil.save("hasil_isotropik_horizontal.jpg")

print("Deteksi tepi Isotropik selesai!")
print("Hasil disimpan sebagai hasil_isotropik_horizontal.jpg")