import cv2
import numpy as np
import matplotlib.pyplot as plt

# ================== INPUT ==================
INPUT_PATH = r"D:\Tugas\Semester 3\PCD\PCD\Citra\citra_rgb.png"      # ganti dengan path citra Anda
# ===========================================

# ---------- 1. Baca citra dan ubah ke keabuan ----------
citra = cv2.imread(INPUT_PATH)
if citra is None:
    raise FileNotFoundError("Citra tidak ditemukan: " + INPUT_PATH)
gray = cv2.cvtColor(citra, cv2.COLOR_BGR2GRAY)
h, w = gray.shape
N = h * w                                   # jumlah seluruh piksel

# ---------- 2. Histogram dan peluang tiap tingkat keabuan ----------
hist = np.bincount(gray.ravel(), minlength=256)
p = hist / N                                # p[i] = peluang keabuan i
mu_total = np.sum(np.arange(256) * p)       # rata-rata keabuan seluruh citra

# ---------- 3. Hitung varians antar-kelas untuk setiap kandidat T ----------
sigma_b2 = np.zeros(256)
w0 = 0.0          # peluang kumulatif kelas 0
jumlah0 = 0.0     # jumlah i * p[i] kumulatif kelas 0

for t in range(256):
    w0 += p[t]
    jumlah0 += t * p[t]
    w1 = 1.0 - w0

    # jika salah satu kelas kosong, varians antar-kelas tidak bermakna
    if w0 == 0 or w1 == 0:
        continue

    mu0 = jumlah0 / w0
    mu1 = (mu_total - jumlah0) / w1
    sigma_b2[t] = w0 * w1 * (mu0 - mu1) ** 2

# ---------- 4. Ambang optimal = T dengan varians antar-kelas terbesar ----------
T = int(np.argmax(sigma_b2))
print("Ukuran citra       :", w, "x", h)
print("Ambang Otsu (manual):", T)

# ---------- 5. Terapkan thresholding: Ki > T -> 255 (putih), selain itu 0 (hitam) ----------
biner = np.zeros_like(gray)
for y in range(h):
    for x in range(w):
        if gray[y, x] > T:
            biner[y, x] = 255

# ---------- 6. Pembanding: fungsi bawaan OpenCV ----------
T_cv, biner_cv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print("Ambang Otsu (OpenCV):", int(T_cv))
print("Hasil manual = OpenCV ?", np.array_equal(biner, biner_cv))

cv2.imwrite("hasil_otsu.png", biner)

# ---------- 7. Tampilkan ----------
fig = plt.figure(figsize=(14, 9))
gs = fig.add_gridspec(2, 6, height_ratios=[1, 1.1])
 
ax_asli = fig.add_subplot(gs[0, 0:2])
ax_asli.imshow(cv2.cvtColor(citra, cv2.COLOR_BGR2RGB))
ax_asli.set_title("Citra asli")
ax_asli.axis("off")
 
ax_gray = fig.add_subplot(gs[0, 2:4])
ax_gray.imshow(gray, cmap="gray", vmin=0, vmax=255)
ax_gray.set_title("Grayscale")
ax_gray.axis("off")
 
ax_hasil = fig.add_subplot(gs[0, 4:6])
ax_hasil.imshow(biner, cmap="gray", vmin=0, vmax=255)
ax_hasil.set_title(f"Otsu's Thresholding (T={T})")
ax_hasil.axis("off")
 
ax_hist = fig.add_subplot(gs[1, 0:3])
ax_hist.bar(range(256), hist, width=1.0, color="k")
ax_hist.axvline(T, color="r", linestyle="--", label=f"T = {T}")
ax_hist.set_title("Histogram dan ambang Otsu")
ax_hist.set_xlabel("Tingkat keabuan")
ax_hist.set_ylabel("Jumlah piksel")
ax_hist.legend()
 
ax_var = fig.add_subplot(gs[1, 3:6])
ax_var.plot(range(256), sigma_b2, color="b")
ax_var.axvline(T, color="r", linestyle="--", label=f"T = {T}")
ax_var.set_title("Varians antar-kelas (maksimum di T)")
ax_var.set_xlabel("T")
ax_var.set_ylabel("Varians antar-kelas")
ax_var.legend()
 
plt.tight_layout()
plt.savefig("langkah_otsu.png", dpi=110)
plt.show()