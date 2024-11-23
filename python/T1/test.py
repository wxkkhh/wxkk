import numpy as np
import cv2
import matplotlib.pyplot as plt

# 透射率模型：计算每个通道的衰减
def transmission(depth_map, beta_r, beta_g, beta_b):
    """
    计算水下图像的衰减效果
    depth_map: 每个像素的深度图，单位为米
    beta_r, beta_g, beta_b: 红色、绿色和蓝色通道的衰减系数
    """
    t_r = np.exp(-beta_r * depth_map)  # 红色通道的透射率
    t_g = np.exp(-beta_g * depth_map)  # 绿色通道的透射率
    t_b = np.exp(-beta_b * depth_map)  # 蓝色通道的透射率
    return t_r, t_g, t_b

# 计算水体影响
def water_effect(t, max_effect=50):
    """
    模拟水体对图像的影响，通常表现为图像的模糊和暗化。
    t: 透射率
    max_effect: 最大影响强度
    """
    return max_effect * (1 - t)  # 散射和吸收效果随透射率降低而增强

# 生成水下图像模型
def underwater_image_model(J, depth_map, beta_r=0.06, beta_g=0.04, beta_b=0.02):
    """
    构建水下图像，计算RGB通道的衰减
    J: 原始图像
    depth_map: 每个像素的深度图，单位为米
    beta_r, beta_g, beta_b: 每个通道的衰减系数
    """
    # 计算不同通道的透射率 t(x)
    t_r, t_g, t_b = transmission(depth_map, beta_r, beta_g, beta_b)

    # 计算水体影响 B(t(x))，这里我们简单模拟为透射率函数
    B_r = water_effect(t_r)  # 红色通道的水体影响
    B_g = water_effect(t_g)  # 绿色通道的水体影响
    B_b = water_effect(t_b)  # 蓝色通道的水体影响

    # 分别计算每个通道的水下图像 I(x)
    I_r = J[..., 0] * t_r + B_r
    I_g = J[..., 1] * t_g + B_g
    I_b = J[..., 2] * t_b + B_b

    # 将三个通道合并
    I = np.stack([I_r, I_g, I_b], axis=-1)

    # 确保输出图像在有效范围内
    I = np.clip(I, 0, 255).astype(np.uint8)

    return I

# 示例：加载原始图像 J 和深度图
J = cv2.imread('d:\\GitHub\\wxkk\\python\\T1\\aaa.jpg')  # 假设图像路径为'underwater_scene.jpg'
J = cv2.cvtColor(J, cv2.COLOR_BGR2RGB)  # 转换为 RGB 格式

# 假设每个像素的深度图，范围从0到100米（实际情况中可通过深度传感器获得）
height, width, _ = J.shape
depth_map = np.linspace(50, 60, width)  # 水平距离（假设为0到100米之间的线性分布）
depth_map = np.tile(depth_map, (height, 1))  # 扩展为图像的尺寸

# 生成水下图像 I(x)
I = underwater_image_model(J, depth_map, beta_r=0.06, beta_g=0.04, beta_b=0.02)

# 显示水下图像
plt.figure(figsize=(10, 10))
plt.subplot(1, 2, 1)
plt.imshow(J)
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(I)
plt.title("Underwater Image with Depth-based Attenuation")
plt.axis('off')

plt.show()
