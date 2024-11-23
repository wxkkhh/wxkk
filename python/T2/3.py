import cv2
import numpy as np
import matplotlib.pyplot as plt

def underwater_image_transformation(image, depth, alpha, beta, Ib):
    """
    将输入的RGB图像基于光传输模型转换为水下图像，支持为每个通道单独设置吸收和散射系数。
    
    参数:
        image: 输入的RGB图像 (BGR格式)。
        depth: 水深 (米)。
        alpha: 吸收系数列表 [alpha_R, alpha_G, alpha_B]。
        beta: 散射系数列表 [beta_R, beta_G, beta_B]。
        Ib: 背景光强度列表 [Ib_R, Ib_G, Ib_B]。
    
    返回:
        transformed_image: 转换后的水下图像。
    """
    # 将图像归一化到 [0, 1]
    image_normalized = image / 255.0

    # 分别对 R, G, B 通道应用光传输模型
    channels = cv2.split(image_normalized)
    transformed_channels = []
    for i, channel in enumerate(channels):
        attenuation_coefficient = alpha[i] + beta[i]
        transformed_channel = channel * np.exp(-attenuation_coefficient * depth) + Ib[i]
        transformed_channels.append(transformed_channel)

    # 合并通道
    transformed_image = cv2.merge(transformed_channels)

    # 将图像裁剪到 [0, 1] 并还原到 [0, 255]
    transformed_image = np.clip(transformed_image, 0, 1) * 255
    transformed_image = transformed_image.astype(np.uint8)

    return transformed_image

# 加载图片 (替换路径为你的水下图片路径)
image_path = "D:\\GitHub\\wxkk\\python\\T4\\Paired\\underwater_dark\\trainB\\264286_00007889.jpg"  # 替换为实际图像路径
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError("图像文件未找到，请检查路径！")

# 定义每个通道的参数
depth = 10  # 水深 (米)

# 吸收系数 (R, G, B)
alpha = [0.03, 0.07, 0.1]

# 散射系数 (R, G, B)
beta = [0.06, 0.08, 0.2]

# 背景光强度 (R, G, B)
Ib = [0.1, 0.15, 0.2]

# 模拟水下转换
transformed_image = underwater_image_transformation(image, depth, alpha, beta, Ib)

# 显示原图和转换后的图像
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title("原始图像")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # 转为 RGB 格式显示
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title(f"水深 {depth} 米的水下图像")
plt.imshow(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB))  # 转为 RGB 格式显示
plt.axis('off')

plt.tight_layout()
plt.show()
