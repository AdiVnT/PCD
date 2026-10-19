```python
from PIL import Image
import math

# Membaca gambar dan mengubah menjadi grayscale
img_asli = Image.open(
    r"C:\Users\adi\Documents\SMT3\pcd\Screenshot 2026-10-04 222533.png"
).convert("L")

# Menampilkan ukuran gambar
lebar, tinggi = img_asli.size
print("Ukuran gambar:", lebar, "x", tinggi)

# Membuat gambar kosong untuk hasil
hasil_h = Image.new("L", (lebar, tinggi))
hasil_v = Image.new("L", (lebar, tinggi))
hasil_gabungan = Image.new("L", (lebar, tinggi))

# Mask Prewitt Horizontal
mask_h = [
    [-1, -1, -1],
    [ 0,  0,  0],
    [ 1,  1,  1]
]

# Mask Prewitt Vertikal
mask_v = [
    [-1,  0,  1],
    [-1,  0,  1],
    [-1,  0,  1]
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

        # Perhitungan Prewitt Horizontal
        nilai_h = (
            p00 * mask_h[0][0] +
            p01 * mask_h[0][1] +
            p02 * mask_h[0][2] +
            p10 * mask_h[1][0] +
            p11 * mask_h[1][1] +
            p12 * mask_h[1][2] +
            p20 * mask_h[2][0] +
            p21 * mask_h[2][1] +
            p22 * mask_h[2][2]
        )

        # Perhitungan Prewitt Vertikal
        nilai_v = (
            p00 * mask_v[0][0] +
            p01 * mask_v[0][1] +
            p02 * mask_v[0][2] +
            p10 * mask_v[1][0] +
            p11 * mask_v[1][1] +
            p12 * mask_v[1][2] +
            p20 * mask_v[2][0] +
            p21 * mask_v[2][1] +
            p22 * mask_v[2][2]
        )

        # Mengambil nilai absolut
        nilai_h = abs(nilai_h)
        nilai_v = abs(nilai_v)

        # Membatasi nilai agar tidak melebihi 255
        nilai_h = min(255, nilai_h)
        nilai_v = min(255, nilai_v)

        # Menggabungkan kedua arah menggunakan rumus gradien
        nilai_g = math.sqrt(nilai_h**2 + nilai_v**2)
        nilai_g = min(255, int(nilai_g))

        # Menyimpan hasil ke masing-masing gambar
        hasil_h.putpixel((x, y), nilai_h)
        hasil_v.putpixel((x, y), nilai_v)
        hasil_gabungan.putpixel((x, y), nilai_g)

# Menampilkan gambar asli dan hasil
img_asli.show()
hasil_h.show()
hasil_v.show()
hasil_gabungan.show()

# Menyimpan hasil
hasil_h.save("hasil_prewitt_horizontal.jpg")
hasil_v.save("hasil_prewitt_vertikal.jpg")
hasil_gabungan.save("hasil_prewitt_gabungan.jpg")

print("Deteksi tepi Prewitt selesai!")
print("Hasil horizontal disimpan sebagai hasil_prewitt_horizontal.jpg")
print("Hasil vertikal disimpan sebagai hasil_prewitt_vertikal.jpg")
print("Hasil gabungan disimpan sebagai hasil_prewitt_gabungan.jpg")
```