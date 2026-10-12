import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(r'D:\Tugas\Semester 3\PCD\gs_20x30.png')

xL, yT = 5, 2
xR, yB = 13, 18

w_baru = xR - xL
h_baru = yB - yT
c = img.shape[2]

img_cropped = np.zeros((h_baru, w_baru, c), dtype=np.uint8)

for y in range(yT, yB):
    for x in range(xL, xR):
        x_baru = x - xL
        y_baru = y - yT

        img_cropped[y_baru, x_baru] = img[y, x]

cv2.imwrite('hasil_cropping.png', img_cropped)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(img, cmap="gray", vmin=0, vmax=255)
axes[0].set_title("Gambar Asli")
axes[0].axis("off")

axes[1].imshow(img_cropped, cmap="gray", vmin=0, vmax=255)
axes[1].set_title("Gambar Hasil Cropping")
axes[1].axis("off")

plt.tight_layout()
plt.show()