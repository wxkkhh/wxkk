import numpy as np
import cv2
import matplotlib.pyplot as plt

# 假设的水下光学参数（可以根据实际环境调整）
alpha_a_base = 0.1  # 吸收系数基础值（1/m）
alpha_s_base = 0.05  # 散射系数基础值（1/m）
max_depth = 100  # 最大深度（单位：米）

# 深度范围设置
depth_interval = 1  # 深度步长（单位：米）
depths = np.arange(0, max_depth + depth_interval, depth_interval)  # 深度数组

# 假设散射系数和吸收系数随深度变化
def alpha_a(z):
    """计算深度 z 处的吸收系数"""
    return alpha_a_base + 0.005 * z  # 随深度增加

def alpha_s(z):
    """计算深度 z 处的散射系数"""
    return alpha_s_base + 0.002 * z  # 随深度增加

def alpha_total(z):
    """计算深度 z 处的总衰减系数"""
    return alpha_a(z) + alpha_s(z)

# 计算光强衰减
def apply_scattering_effect(image, depth):
    """应用水下散射和吸收效果，调整图像的亮度"""
    # 计算对应深度的总衰减系数
    alpha = alpha_total(depth)
    
    # 将图像转换为浮动格式以便处理
    image_float = image.astype(np.float32) / 255.0  # 归一化到 [0, 1]
    
    # 计算衰减因子
    decay_factor = np.exp(-alpha * depth)
    
    # 应用衰减因子到每个像素
    image_decayed = image_float * decay_factor
    
    # 将图像重新缩放回 [0, 255] 范围
    image_decayed = np.clip(image_decayed * 255, 0, 255).astype(np.uint8)
    
    return image_decayed

# 加载原始图像
image = cv2.imread('d:\\GitHub\\wxkk\\python\\T2\\normal4.jpg')  # 加载图像
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换为RGB格式

# 设置一个假设的深度值，表示在水下的某一层
depth = 5  # 假设深度为10米

# 使用水下成像散射模型对图像进行变换
image_underwater = apply_scattering_effect(image_rgb, depth)

# 显示原始图像和水下变换后的图像
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(image_rgb)
axes[0].set_title("原始图像")
axes[0].axis('off')

axes[1].imshow(image_underwater)
axes[1].set_title(f"水下变换图像 (深度 {depth} 米)")
axes[1].axis('off')

plt.show()
