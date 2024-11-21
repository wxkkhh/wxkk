import cv2
import numpy as np

def detect_color_bias_lab(image_path, threshold=100):
    # 读取图像
    image = cv2.imread(image_path)
    
    # 将 BGR 图像转换为 CIE Lab 色彩空间
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # 分离 L, a, b 通道
    L, a, b = cv2.split(image_lab)
    
    # 计算 a 和 b 通道的均值
    a_mean = np.mean(a)
    b_mean = np.mean(b)
    
    print(f"a* mean: {a_mean}")
    print(f"b* mean: {b_mean}")
    
    # 判断是否有色偏
    if a_mean > threshold:
        return "Possible red bias"
    elif a_mean < -threshold:
        return "Possible green bias"
    elif b_mean > threshold:
        return "Possible yellow bias"
    elif b_mean < -threshold:
        return "Possible blue bias"
    else:
        return "No significant color bias"

# 测试图片路径
image_path = 'd:\GitHub\wxkk\python\image_044.png'  # 替换为你的图片路径
print(detect_color_bias_lab(image_path))
