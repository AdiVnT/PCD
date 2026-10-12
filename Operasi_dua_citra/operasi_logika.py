import numpy as np
import cv2
from PIL import Image
import os

def tampilkan_metadata(label, filepath):
    print(f"\n=== METADATA CITRA {label} ===")
    
    with Image.open(filepath) as img_pil:
        format_file = img_pil.format
        mode_ruang = img_pil.mode
        lebar, tinggi = img_pil.size
    
    img_cv = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
    tipe_data = img_cv.dtype
    
    if len(img_cv.shape) == 3:
        channel = img_cv.shape[2]
        jenis = "Berwarna (Multichannel)"
    else:
        channel = 1
        jenis = "Grayscale / Biner (Single Channel)"

    if tipe_data == 'uint8':
        bit_depth = 8
    elif tipe_data == 'uint16':
        bit_depth = 16
    else:
        bit_depth = np.iinfo(tipe_data).bits if np.issubdtype(tipe_data, np.integer) else "Unknown"

    total_depth = bit_depth * channel

    print(f"File         : {os.path.basename(filepath)}")
    print(f"Format       : {format_file}")
    print(f"Resolusi     : {lebar} x {tinggi} piksel")
    print(f"Jenis Citra  : {jenis}")
    print(f"Mode Warna   : {mode_ruang}")
    print(f"Channel      : {channel} Saluran")
    print(f"Tipe Array   : {tipe_data}")
    print(f"Bit Depth    : {bit_depth}-bit per channel")
    print(f"Total Depth  : {total_depth}-bit per piksel (BPP)\n")


path_a = r'D:\Tugas\Semester 3\PCD\biner2.png'
path_b = r'D:\Tugas\Semester 3\PCD\biner1.jpg'

tampilkan_metadata("A", path_a)
tampilkan_metadata("B", path_b)

img_a_asli = cv2.imread(path_a, cv2.IMREAD_UNCHANGED)
img_b_asli = cv2.imread(path_b, cv2.IMREAD_UNCHANGED)

def pastikan_grayscale(img):
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

img_a_gray = pastikan_grayscale(img_a_asli)
img_b_gray = pastikan_grayscale(img_b_asli)

tipe_data = img_a_gray.dtype
nilai_maks = int(np.iinfo(tipe_data).max)
nilai_tengah = nilai_maks // 2

_, img_a_biner = cv2.threshold(img_a_gray, nilai_tengah, nilai_maks, cv2.THRESH_BINARY)
_, img_b_biner = cv2.threshold(img_b_gray, nilai_tengah, nilai_maks, cv2.THRESH_BINARY)

tinggi, lebar = img_a_biner.shape
img_b_biner = cv2.resize(img_b_biner, (lebar, tinggi))

hasil = np.zeros((tinggi, lebar), dtype=tipe_data)

pilihan = input("Pilih operasi logika (AND / OR / XOR / SUB / NOT): ").strip().upper()

match pilihan:
    case "AND":
        for y in range(tinggi):
            for x in range(lebar):
                hasil[y, x] = img_a_biner[y, x] & img_b_biner[y, x]
                
    case "OR":
        for y in range(tinggi):
            for x in range(lebar):
                hasil[y, x] = img_a_biner[y, x] | img_b_biner[y, x]
                
    case "XOR":
        for y in range(tinggi):
            for x in range(lebar):
                hasil[y, x] = img_a_biner[y, x] ^ img_b_biner[y, x]
                
    case "SUB":
        for y in range(tinggi):
            for x in range(lebar):
                pengurangan = int(img_a_biner[y, x]) - int(img_b_biner[y, x])
                hasil[y, x] = max(0, pengurangan)
                
    case "NOT":
        for y in range(tinggi):
            for x in range(lebar):
                hasil[y, x] = nilai_maks - img_a_biner[y, x]
                
    case _:
        print("Pilihan operasi tidak valid!")

# Menampilkan Hasil
if pilihan in ["AND", "OR", "XOR", "SUB", "NOT"]:
    cv2.namedWindow(f"Hasil Operasi {pilihan}", cv2.WINDOW_NORMAL)
    cv2.imshow(f"Hasil Operasi {pilihan}", hasil)
    cv2.waitKey(0)
    cv2.destroyAllWindows()