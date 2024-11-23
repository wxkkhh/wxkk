import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import convolve

# 全局定义深度变量，方便统一调整
GLOBAL_DEPTH = [1.0, 5.0, 10.0]  # 可以定义多个深度值，便于计算和对比

def calculate_attenuation_coefficients(beta, depths):
    return [np.exp(-beta * depth) for depth in depths]

def apply_color_cast_model(image, beta_red=0.8, beta_green=0.6, depths=GLOBAL_DEPTH):
    images = []
    for depth in depths:
        # 将图像分割为 R、G、B 通道
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        
        # 模型公式： J_c(x, y) = I_c(x, y) * exp(-beta_c * d)
        r = r * np.exp(-beta_red * depth)
        g = g * np.exp(-beta_green * depth)
        b = b * np.exp(-0 * depth)  # 蓝光吸收最小，因此不进行衰减
        
        # 限制值范围在 [0, 255]
        r = np.clip(r, 0, 255)
        g = np.clip(g, 0, 255)
        b = np.clip(b, 0, 255)
        
        # 合并通道
        color_cast_image = np.stack([r, g, b], axis=-1).astype(np.uint8)
        images.append(color_cast_image)
    return images

def apply_low_light_model(image, beta=0.7, depths=GLOBAL_DEPTH, A=0.5):
    images = []
    for depth in depths:
        # 计算光线传输率 t(x, y) = exp(-beta * d)
        t = np.exp(-beta * depth)
        
        # 将图像分割为 R、G、B 通道
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        
        # 计算观察到的图像亮度 L(x, y) = J(x, y) * t(x, y) + A * (1 - t(x, y))
        r = r * t + A * (1 - t) * 255
        g = g * t + A * (1 - t) * 255
        b = b * t + A * (1 - t) * 255
        
        # 限制值范围在 [0, 255]
        r = np.clip(r, 0, 255)
        g = np.clip(g, 0, 255)
        b = np.clip(b, 0, 255)
        
        # 合并通道
        low_light_image = np.stack([r, g, b], axis=-1).astype(np.uint8)
        images.append(low_light_image)
    return images

def apply_blur_model(image, rho=0.5, depths=GLOBAL_DEPTH):
    images = []
    for depth in depths:
        # 计算散射方差：sigma_blur^2 ∝ rho * d
        sigma_blur = rho * depth
        
        # 创建正向散射点扩散函数 (PSF)，使用高斯模糊近似
        size = int(6 * sigma_blur + 1)  # 根据 sigma 计算卷积核大小
        if size % 2 == 0:
            size += 1  # 保证卷积核大小为奇数
        
        psf = np.ones((size, size)) / (size * size)  # 简化为均值滤波器来模拟模糊
        
        # 应用卷积（模糊效果）
        blurred_image = np.zeros_like(image)
        for i in range(3):  # 对 R、G、B 三个通道分别进行卷积
            blurred_image[:, :, i] = convolve(image[:, :, i], psf, mode='reflect')
        
        # 限制值范围在 [0, 255]
        blurred_image = np.clip(blurred_image, 0, 255).astype(np.uint8)
        images.append(blurred_image)
    return images

# 读取图像
image_path = 'd:\\GitHub\\wxkk\\python\\T1\\aaa.jpg'  # 替换为你的图像路径
input_image = cv2.imread(image_path)
input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

# 使用基于物理模型的方法生成具有色偏的图像
generated_color_cast_images = apply_color_cast_model(input_image)

# 使用光线不足模型生成低光图像
generated_low_light_images = apply_low_light_model(input_image)

# 使用模糊模型生成模糊图像
generated_blur_images = apply_blur_model(input_image)

# 显示输入和生成的图像
plt.figure(figsize=(20, 15))
plt.subplot(3, len(GLOBAL_DEPTH) + 1, 1)
plt.title("Input Image")
plt.imshow(input_image)
for i, depth in enumerate(GLOBAL_DEPTH):
    plt.subplot(3, len(GLOBAL_DEPTH) + 1, i + 2)
    plt.title(f"Color Cast Depth {depth}")
    plt.imshow(generated_color_cast_images[i])
    
for i, depth in enumerate(GLOBAL_DEPTH):
    plt.subplot(3, len(GLOBAL_DEPTH) + 1, len(GLOBAL_DEPTH) + 2 + i)
    plt.title(f"Low Light Depth {depth}")
    plt.imshow(generated_low_light_images[i])
    
for i, depth in enumerate(GLOBAL_DEPTH):
    plt.subplot(3, len(GLOBAL_DEPTH) + 1, 2 * len(GLOBAL_DEPTH) + 3 + i)
    plt.title(f"Blur Depth {depth}")
    plt.imshow(generated_blur_images[i])

plt.show()
