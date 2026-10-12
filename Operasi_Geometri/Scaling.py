import cv2
import numpy as np

img = cv2.imread('gs_20x30.png')
h, w, c = img.shape  

skala_x = float(input("Masukkan skala untuk sumbu x (Sh): "))
skala_y = float(input("Masukkan skala untuk sumbu y (Sv): "))

lebar_baru = int(w * skala_x)
tinggi_baru = int(h * skala_y)

img_scaled = np.zeros((tinggi_baru, lebar_baru, c), dtype=np.uint8)

for y_baru in range(tinggi_baru):
    for x_baru in range(lebar_baru):
        x_lama = int(x_baru / skala_x)
        y_lama = int(y_baru / skala_y)

        x_lama = min(x_lama, w - 1)
        y_lama = min(y_lama, h - 1)

        img_scaled[y_baru, x_baru] = img[y_lama, x_lama]

cv2.imwrite('hasil_skalasi_mulus.png', img_scaled)
print("Skalasi selesai tanpa piksel hitam!")