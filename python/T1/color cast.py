from PIL import Image
import numpy as np
from skimage.color import rgb2lab

def convert_to_24bpp_rgb(image_path):
    """
    将图片转换为 24 位 RGB 格式并返回图像对象。
    """
    # 打开图像
    image = Image.open(image_path)
    
    # 转换为 RGB 模式（24 位）
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

def calculate_color_cast(image):
    """
    计算图片的偏色因子，基于 CIE Lab 色彩空间的 A 和 B 通道。
    """
    # 将图像转换为 numpy 数组
    image_np = np.array(image)
    
    # 转换为 Lab 色彩空间
    lab_image = rgb2lab(image_np / 255.0)  # RGB to Lab, scale to [0, 1]
    
    # 获取 Lab 图像的 A 和 B 分量
    A = lab_image[:, :, 1]
    B = lab_image[:, :, 2]
    
    # 计算平均值
    avg_A = np.mean(A)
    avg_B = np.mean(B)
    
    # 计算 A 和 B 的绝对偏离值（代替方差方法）
    dev_A = np.mean(np.abs(A - avg_A))
    dev_B = np.mean(np.abs(B - avg_B))
    
    # 计算偏色因子
    color_cast_factor = np.sqrt(avg_A**2 + avg_B**2) / np.sqrt(dev_A**2 + dev_B**2)
    return color_cast_factor

def main(image_path):
    # 将图像转换为 24 位 RGB 格式
    image = convert_to_24bpp_rgb(image_path)
    
    # 计算偏色因子
    color_cast_factor = calculate_color_cast(image)
    
    print(f"Color Cast Factor: {color_cast_factor}")
    return color_cast_factor

# 示例用法
image_path = "d:\GitHub\wxkk\python\image_364.jpg"  # 替换为实际图片路径
main(image_path)
