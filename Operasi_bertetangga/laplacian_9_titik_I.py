
from PIL import Image
import numpy as np


img_asli = Image.open(
    r"C:\Users\adi\Documents\SMT3\pcd\Screenshot 2026-10-04 222533.png"
).convert("L")

lebar, tinggi = img_asli.size

img = np.array(img_asli, dtype=np.int32)


mask = [
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
]


hasil = np.zeros((tinggi, lebar), dtype=np.uint8)

for y in range(1, tinggi - 1):
    for x in range(1, lebar - 1):

        nilai = 0

        # Perhitungan 3x3
        for j in range(-1, 2):
            for i in range(-1, 2):
                nilai += img[y + j, x + i] * mask[j + 1][i + 1]

      
        nilai = abs(nilai)

       
        nilai = min(255, nilai)

        hasil[y, x] = nilai


hasil = Image.fromarray(hasil)


img_asli.show()
hasil.show()

hasil.save("hasil_laplacian_9_titik_I.jpg")

print("Laplacian 9 titik I selesai!")
print("Hasil disimpan sebagai hasil_laplacian_9_titik_I.jpg")