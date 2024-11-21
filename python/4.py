from PIL import Image
import numpy as np

def rgb_to_lab(image):
    # 将 RGB 图像转换为 Lab 图像
    from skimage.color import rgb2lab
    return rgb2lab(image)

def get_color_cast_factor(image_path):
    # 读取图像
    image = Image.open(image_path)
    
    # 确保图像是 RGB 格式
    if image.mode != 'RGB':
        raise ValueError("Only Support RGB format Image.")
    
    # 将图像转换为 numpy 数组
    image_np = np.array(image)
    
    # 转换为 Lab 色彩空间
    lab_image = rgb_to_lab(image_np / 255.0)  # RGB to Lab, scale to [0, 1]
    
    # 获取 Lab 图像的 A 和 B 分量
    A = lab_image[:, :, 1]
    B = lab_image[:, :, 2]
    
    # 计算 A 和 B 分量的直方图
    hist_A, _ = np.histogram(A, bins=256, range=(-128, 127))
    hist_B, _ = np.histogram(B, bins=256, range=(-128, 127))
    
    # 计算 A 和 B 分量的总和
    sum_A = np.sum(A)
    sum_B = np.sum(B)
    
    # 计算平均值
    avg_A = sum_A / (image.width * image.height) - 128  # A 需要归一化
    avg_B = sum_B / (image.width * image.height) - 128  # B 需要归一化
    
    # 计算方差
    msq_A = np.sum(np.abs(np.arange(256) - avg_A - 128) * hist_A) / (image.width * image.height)
    msq_B = np.sum(np.abs(np.arange(256) - avg_B - 128) * hist_B) / (image.width * image.height)
    
    # 计算 Color Cast Factor
    color_cast_factor = np.sqrt(avg_A ** 2 + avg_B ** 2) / np.sqrt(msq_A ** 2 + msq_B ** 2)
    
    return color_cast_factor

# 测试代码
image_path = 'd:\GitHub\wxkk\python\image_044.png'  # 替换为实际图片路径
color_cast_factor = get_color_cast_factor(image_path)
print(f"Color Cast Factor: {color_cast_factor}")
