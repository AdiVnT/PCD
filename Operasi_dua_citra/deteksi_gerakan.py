from PIL import Image
import numpy as np


img_a_asli = Image.open(
    r"C:\Users\adi\Documents\SMT3\pcd\image 1.jpg"
).convert("RGB")

img_b_asli = Image.open(
    r"C:\Users\adi\Documents\SMT3\pcd\image 2.jpg"
).convert("RGB")


print("Ukuran gambar A:", img_a_asli.size)
print("Ukuran gambar B:", img_b_asli.size)

lebar, tinggi = img_a_asli.size
img_b = img_b_asli.resize((lebar, tinggi))
img_a = img_a_asli


wa = 1
wb = -1


hasil = Image.new("RGB", (lebar, tinggi))

for y in range(tinggi):
    for x in range(lebar):

      
        rA, gA, bA = img_a.getpixel((x, y))

      
        rB, gB, bB = img_b.getpixel((x, y))

       
        r = abs(int(wa * rA + wb * rB))
        g = abs(int(wa * gA + wb * gB))
        b = abs(int(wa * bA + wb * bB))

        
        hasil.putpixel((x, y), (r, g, b))


img_a.show()
img_b.show()
hasil.show()


hasil.save("hasil_deteksi_gerakan.jpg")

print("Deteksi gerakan selesai!")
print("Hasil disimpan sebagai hasil_deteksi_gerakan.jpg")