import struct
import cv2

nama_file = r"D:\Tugas\Semester 3\PCD\gs.jpg"  

with open(nama_file, "rb") as f:
    d = f.read()

print("=== INFORMASI METADATA DARI HEADER BINER ===")

if d[:8] == b"\x89PNG\r\n\x1a\n":
    lebar, tinggi = struct.unpack(">II", d[16:24])
    tipe_warna = {0: "Grayscale", 2: "RGB", 3: "Indexed",
                  4: "Grayscale+Alpha", 6: "RGBA"}
    print("Format File  : PNG")
    print(f"Resolusi     : {lebar} x {tinggi} piksel")
    print(f"Bit Depth    : {d[24]}-bit")
    print(f"Tipe Warna   : {tipe_warna.get(d[25], 'Unknown')}")

elif d[:2] == b"BM":
    lebar, tinggi = struct.unpack("<ii", d[18:26])
    bit_depth = struct.unpack("<H", d[28:30])[0]
    print("Format File  : BMP")
    print(f"Resolusi     : {lebar} x {abs(tinggi)} piksel")
    print(f"Bit Depth    : {bit_depth}-bit")

elif d[:2] == b"\xff\xd8":
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
           0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    i = 2
    ditemukan = False
    while i < len(d) - 9:
        if d[i] != 0xFF:
            i += 1
        elif d[i + 1] in sof:
            tinggi, lebar = struct.unpack(">HH", d[i + 5:i + 9])
            print("Format File  : JPEG")
            print(f"Resolusi     : {lebar} x {tinggi} piksel")
            print(f"Bit Depth    : {d[i + 4]}-bit per kanal")
            print(f"Jumlah Kanal : {d[i + 9]} (1=Grayscale, 3=RGB, 4=CMYK)")
            ditemukan = True
            break
        elif d[i + 1] in (0x00, 0xD8, 0xD9) or 0xD0 <= d[i + 1] <= 0xD7:
            i += 2
        elif d[i + 1] == 0xFF:
            i += 1
        else:
            i += 2 + struct.unpack(">H", d[i + 2:i + 4])[0]
    if not ditemukan:
        print("Error: Header JPEG tidak ditemukan.")

else:
    print("Error: Format berkas tidak dikenali atau header tidak didukung.")

print("\n=== PEMBACAAN INTENSITAS PIKSEL ===")
img = cv2.imread(nama_file, cv2.IMREAD_UNCHANGED)

if img is None:
    print("Error: Berkas tidak dapat dibuka oleh OpenCV.")
else:
    h, w = img.shape[:2]
    for y in range(h):
        for x in range(w):
            print(f"Titik (x={x}, y={y}) -> Intensitas: {img[y, x]}")