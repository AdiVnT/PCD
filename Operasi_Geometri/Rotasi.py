import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

img = cv2.imread(r'D:\Tugas\Semester 3\PCD\gs.jpg')

h, w, c = img.shape

print("Pilih derajat rotasi : 1. 90 derajat  2. 180 derajat 3. CCW")

pilihan = input("Pilih : ")

if pilihan == "1" or pilihan.lower() == "90":
    w_baru = h
    h_baru = w
    
    img_rotasi = np.zeros((h_baru, w_baru, c), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            
            x_baru = w_baru - 1 - y
            y_baru = x
            
            img_rotasi[y_baru, x_baru] = img[y, x]

    cv2.imwrite('rotasi_90.png', img_rotasi)
    print("Rotasi 90 derajat selesai disimpan sebagai 'rotasi_90.png'")

elif pilihan == "2" or pilihan.lower() == "180":
    w_baru = w
    h_baru = h

    img_rotasi = np.zeros((h_baru, w_baru, c), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            
            x_baru = w_baru - 1 - x
            y_baru = h_baru - 1 - y
            
            img_rotasi[y_baru, x_baru] = img[y, x]

    cv2.imwrite('rotasi_180.png', img_rotasi)
    print("Rotasi 180 derajat selesai disimpan sebagai 'rotasi_180.png'")

elif pilihan == "3" or pilihan.lower() == "bebas":
    sudut = float(input("Masukkan derajat rotasi bebas berlawanan arah jarum jam (contoh: 45): "))
    theta = math.radians(sudut)

    w_baru = int(abs(w * math.cos(theta)) + abs(h * math.sin(theta)))
    h_baru = int(abs(w * math.sin(theta)) + abs(h * math.cos(theta)))

    img_rotasi = np.zeros((h_baru, w_baru, c), dtype=np.uint8)

    cx, cy = w // 2, h // 2
    cx_baru, cy_baru = w_baru // 2, h_baru // 2

    for y in range(h):
        for x in range(w):
            
            x_geser = x - cx
            y_geser = y - cy
            
            x_rotasi = (x_geser * math.cos(theta)) + (y_geser * math.sin(theta))
            y_rotasi = -(x_geser * math.sin(theta)) + (y_geser * math.cos(theta))
            
            x_akhir = int(x_rotasi + cx_baru)
            y_akhir = int(y_rotasi + cy_baru)
            
            if 0 <= x_akhir < w_baru and 0 <= y_akhir < h_baru:
                img_rotasi[y_akhir, x_akhir] = img[y, x]

    cv2.imwrite('rotasi_bebas.png', img_rotasi)
    print(f"Rotasi bebas {sudut} derajat CCW selesai disimpan sebagai 'rotasi_bebas.png'")

else:
    print("Pilihan tidak valid. Silakan masukkan angka 1, 2, atau 3.")

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].imshow(img, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Gambar Asli")
axes[0, 0].axis("off")

axes[0, 1].imshow(img_rotasi, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title(f"Gambar Hasil (Rotasi {pilihan} derajat)")
axes[0, 1].axis("off")

plt.tight_layout()
plt.show()