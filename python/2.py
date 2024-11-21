import cv2
import numpy as np
import matplotlib.pyplot as plt


def detect_color_bias_by_ratio(image_path, threshold=1.0):
    # 读取图像
    image = cv2.imread(image_path)
    
    # 分离出 RGB 各个通道
    (B, G, R) = cv2.split(image)
    
    # 计算 R/G, R/B, G/B 比值
    b_r = np.mean(B) / np.mean(R)
    b_g = np.mean(B) / np.mean(G)
    g_b = np.mean(G) / np.mean(B)
    g_r = np.mean(G) / np.mean(R)
    
    print(f"B/R ratio: {b_r}")
    print(f"B/G ratio: {b_g}")
    print(f"G/B ratio: {g_b}")
    print(f"G/R ratio: {g_r}")
    
    # 根据比值判断是否有色偏
        
    if b_r > threshold or b_g > threshold:
        return "Possible blue bias"
    elif g_r > threshold or g_b > threshold:
        return "Possible green bias"


    

# 测试图片路径
image_path = 'd:\GitHub\wxkk\python\image_376.jpg'
print(detect_color_bias_by_ratio(image_path))

