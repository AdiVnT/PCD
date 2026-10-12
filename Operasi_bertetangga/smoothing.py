import cv2
import numpy as np

path_file = r"D:\Tugas\Semester 3\PCD\image.png" 

img = cv2.imread(path_file, cv2.IMREAD_GRAYSCALE)

if img is None:
    print(f"Gagal memuat gambar! Pastikan file '{path_file}' ada di lokasi yang tepat.")
    exit()

h, w = img.shape

img_smooth = img.copy()

print("Pilih jenis mask penghalusan:")
print("5  -> 5 titik bertetangga (bentuk silang)")
print("9  -> 9 titik bertetangga (matriks 3x3)")
print("25 -> 25 titik bertetangga (matriks 5x5)")
pilihan = input("Masukkan angka pilihan (5 / 9 / 25): ").strip()

match pilihan:
    case "5":
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                total = (int(img[y, x]) + 
                         int(img[y-1, x]) + int(img[y+1, x]) + 
                         int(img[y, x-1]) + int(img[y, x+1]))
                img_smooth[y, x] = total // 5
                
    case "9":
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                total = 0
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        total += int(img[y+j, x+i])
                img_smooth[y, x] = total // 9
                
    case "25":
        for y in range(2, h - 2):
            for x in range(2, w - 2):
                total = 0
                for j in range(-2, 3):
                    for i in range(-2, 3):
                        total += int(img[y+j, x+i])
                img_smooth[y, x] = total // 25
                
    case _:
        print("Pilihan tidak valid! Program dihentikan.")
        exit()

nama_output = f'hasil_smoothing_{pilihan}titik.png'
cv2.imwrite(nama_output, img_smooth)
print(f"Selesai! Gambar berhasil dihaluskan dan disimpan sebagai '{nama_output}'.")