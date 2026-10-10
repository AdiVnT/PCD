import numpy as np
import cv2

# Membaca gambar
img_a_asli = cv2.imread(
    r"C:\Users\adi\Documents\SMT3\pcd\WhatsApp Image 2026-09-22 at 11.56.03.jpeg",
    cv2.IMREAD_COLOR
)

img_b_asli = cv2.imread(
    r"C:\Users\adi\Documents\SMT3\pcd\WhatsApp Image 2026-09-22 at 11.56.04 (1).jpeg",
    cv2.IMREAD_COLOR
)

# Mengecek apakah gambar berhasil dibaca
if img_a_asli is None or img_b_asli is None:
    print("Gambar tidak ditemukan!")
    exit()

# Menyamakan ukuran gambar B dengan gambar A
tinggi, lebar = img_a_asli.shape[:2]

img_b = cv2.resize(img_b_asli, (lebar, tinggi))
img_a = img_a_asli

# Bobot masing-masing gambar
wa = 0.5
wb = 0.5

# Memastikan jumlah bobot = 1
if wa + wb != 1:
    print("Jumlah bobot harus sama dengan 1!")
    exit()

# Membuat gambar kosong untuk hasil
hasil = np.zeros((tinggi, lebar, 3), dtype=np.uint8)

# Proses blending secara manual
# Rumus:
# C(x,y) = wa * A(x,y) + wb * B(x,y)

for y in range(tinggi):
    for x in range(lebar):

        # Mengambil nilai piksel gambar A
        bA, gA, rA = img_a[y, x]

        # Mengambil nilai piksel gambar B
        bB, gB, rB = img_b[y, x]

        # Rumus blending untuk setiap channel
        b = int(wa * bA + wb * bB)
        g = int(wa * gA + wb * gB)
        r = int(wa * rA + wb * rB)

        # Menyimpan hasil
        hasil[y, x] = [b, g, r]


# Menampilkan hasil
cv2.namedWindow("Gambar A", cv2.WINDOW_NORMAL)
cv2.namedWindow("Gambar B", cv2.WINDOW_NORMAL)
cv2.namedWindow("Hasil Blending", cv2.WINDOW_NORMAL)

cv2.imshow("Gambar A", img_a)
cv2.imshow("Gambar B", img_b)
cv2.imshow("Hasil Blending", hasil)

cv2.waitKey(0)
cv2.destroyAllWindows()