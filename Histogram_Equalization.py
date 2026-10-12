import cv2
import numpy as np
import matplotlib.pyplot as plt


image = cv2.imread(
    "image.png",
    cv2.IMREAD_ANYDEPTH
)

if image is None:
    print("Gambar tidak ditemukan.")
    exit()

# Jika gambar 3 channel, ubah ke grayscale
if image.ndim == 3:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

height, width = image.shape

# Jumlah level grayscale sesuai bit depth asli gambar
L = int(np.iinfo(image.dtype).max) + 1

# HITUNG HISTOGRAM CITRA ASLI
hist_before = np.zeros(L, dtype=np.int32)

for y in range(height):
    for x in range(width):
        pixel = image[y, x]
        hist_before[pixel] += 1


# HITUNG DISTRIBUSI KUMULATIF
cumulative = np.zeros(L, dtype=np.int32)

cumulative[0] = hist_before[0]

for i in range(1, L):
    cumulative[i] = (
        cumulative[i - 1] +
        hist_before[i]
    )


# HITUNG MAPPING
# Ko = round((L-1) * Ci / (h*w))
total_pixels = height * width

mapping = np.zeros(L, dtype=image.dtype)

for i in range(L):
    ci = cumulative[i]
    value = round(
        ((L - 1) * ci) /
        total_pixels
    )
    mapping[i] = np.clip(value, 0, L - 1)

# TERAPKAN MAPPING
output = np.zeros_like(image)

for y in range(height):
    for x in range(width):

        pixel = image[y, x]

        output[y, x] = mapping[pixel]

# HITUNG HISTOGRAM HASIL
hist_after = np.zeros(256, dtype=np.int32)

for y in range(height):
    for x in range(width):
        pixel = output[y, x]
        hist_after[pixel] += 1

# BUAT SATU WINDOW
plt.figure(figsize=(14, 8))


# Gambar asli
plt.subplot(2, 2, 1)

plt.imshow(image, cmap="gray")
plt.title("Citra Asli")
plt.axis("off")


# Gambar hasil equalization
plt.subplot(2, 2, 2)

plt.imshow(output, cmap="gray")
plt.title("Histogram Equalization")
plt.axis("off")


# Histogram asli
plt.subplot(2, 2, 3)

plt.bar(
    range(256),
    hist_before,
    width=1
)

plt.title("Histogram Sebelum")
plt.xlabel("Gray Level")
plt.ylabel("Frekuensi")
plt.xlim(0, 255)


# Histogram hasil
plt.subplot(2, 2, 4)

plt.bar(
    range(256),
    hist_after,
    width=1
)

plt.title("Histogram Sesudah")
plt.xlabel("Gray Level")
plt.ylabel("Frekuensi")
plt.xlim(0, 255)

cv2.imwrite("hasil_equalization.jpg", output)
plt.savefig("perbandinganequalization.png")

plt.tight_layout()

plt.show()