import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取 PNG 格式的图像
#image = cv2.imread('image.png')  # 这里替换成你自己的 PNG 图像路径
image = cv2.imread(r"d:\GitHub\wxkk\python\image_079.png")
if image is None:
    print("Image not found or unable to read.")
# 将图像从 BGR 转换为 RGB，因为 OpenCV 默认读取的是 BGR 格式
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 计算每个通道的直方图
color = ('r', 'g', 'b')  # 定义三个通道
plt.figure(figsize=(12, 6))

# 对每个通道的直方图进行归一化
for i, col in enumerate(color):
    hist = cv2.calcHist([image_rgb], [i], None, [256], [0, 256])
    hist = cv2.normalize(hist, hist).flatten()  # 归一化并展平直方图
    plt.subplot(1, 3, 1)
    plt.plot(hist, color=col)
    plt.title(f'{col.upper()} Channel Histogram')
    plt.xlim([0, 256])

plt.tight_layout()
plt.show()

