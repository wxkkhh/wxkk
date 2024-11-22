import cv2
import numpy as np
import matplotlib.pyplot as plt

def underwater_imaging_model(image, depth=5, beta=(0.62146081, 0.12983174, 0.19618451), background_light=(0.2, 0.5, 0.7)):
    """
    模拟水下成像模型。
    
    参数：
        image: 输入图像（RGB）。
        depth: 水深（以米为单位）。
        beta: 光衰减系数（R, G, B）。
        background_light: 背景光强度（R, G, B）。
        
    返回：
        underwater_image: 模拟的水下图像。
    """
    # 归一化图像
    image = image / 255.0
    h, w, c = image.shape
    
    # 转换为浮点型
    beta = np.array(beta).reshape(1, 1, 3)
    background_light = np.array(background_light).reshape(1, 1, 3)
    
    # 计算透射率
    transmission = np.exp(-beta * depth)
    
    # 模拟水下图像
    underwater_image = image * transmission + background_light * (1 - transmission)
    underwater_image = np.clip(underwater_image, 0, 1)  # 保证在 [0, 1] 范围内
    
    # 转换回 [0, 255]
    underwater_image = (underwater_image * 255).astype(np.uint8)
    return underwater_image

def display_images(original, simulated):
    """显示原始图像和水下模拟图像"""
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis("off")
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(simulated, cv2.COLOR_BGR2RGB))
    plt.title("Underwater Simulated Image")
    plt.axis("off")
    plt.show()

# 测试代码
image_path = 'd:\\GitHub\\wxkk\\python\\T2\\normal4.jpg'  # 替换为实际图像路径
image = cv2.imread(image_path)

# 模拟水下图像
simulated_image = underwater_imaging_model(image, depth=5)

# 显示结果
display_images(image, simulated_image)
