import cv2
import numpy as np

path_file = r"C:\Users\Diandra Aresta\Pictures\Screenshots\image.png"

img = cv2.imread(path_file, cv2.IMREAD_GRAYSCALE)

if img is None:
    print(f"Gagal memuat gambar! Pastikan file '{path_file}' ada di lokasi yang tepat.")
    exit()

h, w = img.shape

img_sharp = img.copy()

print("--- OPERASI PENAJAMAN CITRA (SHARPENING) ---")
print("Pilih jenis mask penajaman:")
print("5 -> Mask 5 titik (tetangga silang)")
print("9 -> Mask 9 titik (matriks 3x3)")
pilihan_mask = input("Masukkan pilihan mask (5 / 9): ").strip()

try:
    alpha = float(input("Masukkan nilai derajat penajaman (alpha, contoh: 1 atau 0.5): "))
except ValueError:
    print("Nilai alpha harus berupa angka! Program dihentikan.")
    exit()

match pilihan_mask:
    case "5":
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                p_pusat = float(img[y, x])
                p_atas  = float(img[y-1, x])
                p_bawah = float(img[y+1, x])
                p_kiri  = float(img[y, x-1])
                p_kanan = float(img[y, x+1])
                
                hasil_kalkulasi = ( (0 * p_atas) + (-alpha * p_kiri) + 
                                    ((1 + 4 * alpha) * p_pusat) + 
                                    (-alpha * p_kanan) + (0 * p_bawah) )
                
                img_sharp[y, x] = np.clip(hasil_kalkulasi, 0, 255)

    case "9":
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                p_pusat = float(img[y, x])
                
                total_tetangga = ( float(img[y-1, x-1]) + float(img[y-1, x]) + float(img[y-1, x+1]) +
                                   float(img[y, x-1])   +                       float(img[y, x+1])   +
                                   float(img[y+1, x-1]) + float(img[y+1, x]) + float(img[y+1, x+1]) )
                
                hasil_kalkulasi = ((1 + 8 * alpha) * p_pusat) + (-alpha * total_tetangga)
                
                img_sharp[y, x] = np.clip(hasil_kalkulasi, 0, 255)

    case _:
        print("Pilihan mask tidak valid! Program dihentikan.")
        exit()

nama_output = f'hasil_sharpening_{pilihan_mask}titik_alpha{alpha}.png'
cv2.imwrite(nama_output, img_sharp)
print(f"Selesai! Gambar berhasil ditajamkan dan disimpan sebagai '{nama_output}'.")