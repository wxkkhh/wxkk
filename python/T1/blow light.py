import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_low_brightness(image_path, brightness_threshold=50, low_brightness_ratio=0.6):
    """
    检测图像是否亮度不足，并绘制灰度分布直方图。
    
    参数：
        image_path: 图像文件路径。
        brightness_threshold: 低亮度阈值（默认50，0为全黑，255为全白）。
        low_brightness_ratio: 低亮度像素比例阈值（默认0.6，即60%以下为亮度不足）。
        
    返回：
        is_low_brightness: 是否亮度不足（布尔值）。
    """
    # 读取图像并转换为灰度
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("无法读取图像，请检查路径是否正确。")
    
    # 计算灰度直方图
    hist, bins = np.histogram(image.ravel(), bins=256, range=(0, 256))
    
    # 计算低亮度像素比例
    low_brightness_pixels = np.sum(hist[:brightness_threshold])  # 灰度值低于阈值的像素数
    total_pixels = image.size  # 图像总像素数
    low_brightness_ratio_actual = low_brightness_pixels / total_pixels
    
    # 判断是否亮度不足
    is_low_brightness = low_brightness_ratio_actual > low_brightness_ratio
    
    # 绘制灰度图和直方图
    plt.figure(figsize=(12, 6))
    
    # 显示灰度图像
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title("Gray Image")
    plt.axis("off")
    
    # 绘制灰度直方图
    plt.subplot(1, 2, 2)
    plt.bar(bins[:-1], hist, width=1, color='gray', edgecolor='black')
    plt.title("Gray Level Distribution")
    plt.xlabel("Gray Level")
    plt.ylabel("Pixel Count")
    plt.axvline(x=brightness_threshold, color='red', linestyle='--', label='Brightness Threshold')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # 打印检测结果
    print(f"低亮度像素比例: {low_brightness_ratio_actual:.2%}")
    print(f"是否亮度不足: {'是' if is_low_brightness else '否'}")
    
    return is_low_brightness

# 示例用法
image_path = "d:\GitHub\wxkk\python\\pexel2.jpg"  # 替换为你的图像路径
detect_low_brightness(image_path)
