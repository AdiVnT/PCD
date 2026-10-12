from PIL import Image

img_asli = Image.open(
    r"C:\Users\adi\Documents\SMT3\pcd\Screenshot 2026-10-04 222533.png"
).convert("L")
lebar, tinggi = img_asli.size

print("Ukuran gambar:", lebar, "x", tinggi)

hasil = Image.new("L", (lebar, tinggi))

mask = [
    [-1, -2, -1],
    [ 0,  0,  0],
    [ 1,  2,  1]
]

for y in range(1, tinggi - 1):
    for x in range(1, lebar - 1):

        p00 = img_asli.getpixel((x - 1, y - 1))
        p01 = img_asli.getpixel((x,     y - 1))
        p02 = img_asli.getpixel((x + 1, y - 1))

        p10 = img_asli.getpixel((x - 1, y))
        p11 = img_asli.getpixel((x,     y))
        p12 = img_asli.getpixel((x + 1, y))

        p20 = img_asli.getpixel((x - 1, y + 1))
        p21 = img_asli.getpixel((x,     y + 1))
        p22 = img_asli.getpixel((x + 1, y + 1))

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

        nilai = abs(nilai)

        nilai = min(255, nilai)

        hasil.putpixel((x, y), nilai)

img_asli.show()
hasil.show()

hasil.save("hasil_sobel_horizontal.jpg")

print("Deteksi tepi Sobel horizontal selesai!")
print("Hasil disimpan sebagai hasil_sobel_horizontal.jpg")