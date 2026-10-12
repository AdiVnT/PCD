import cv2
import numpy as np

img = cv2.imread(r"D:\Tugas\Semester 3\PCD\gs.jpg")

h, w, c = img.shape

img_horisontal = np.zeros_like(img)
img_vertikal = np.zeros_like(img)
img_kombinasi = np.zeros_like(img)

pilihan = input("1. Horisontal\n" "2. Vertikal\n" "3. Kombinasi\nPilih jenis pencerminan: ")
for y in range(h):
    for x in range(w):
        if pilihan == "1" or pilihan.lower() == "horisontal":
         x_baru = w - 1 - x
         y_baru = y
         img_horisontal[y_baru, x_baru] = img[y, x]
        

        elif pilihan == "2" or pilihan.lower() == "vertikal":
         x_baru = x
         y_baru = h - 1 - y
         img_vertikal[y_baru, x_baru] = img[y, x]

        elif pilihan == "3" or pilihan.lower() == "kombinasi":
         x_baru = w - 1 - x
         y_baru = h - 1 - y
         img_kombinasi[y_baru, x_baru] = img[y, x]

if pilihan == "1" or pilihan.lower() == "horisontal":
    cv2.imwrite('horisontal.png', img_horisontal)
    
elif pilihan == "2" or pilihan.lower() == "ertikal":
    cv2.imwrite('vertikal.png', img_vertikal)

elif pilihan =="3" or pilihan.lower() == "kombinasi":
    cv2.imwrite('kombinasi.png', img_kombinasi)

print("Pencerminan selesai disimpan")