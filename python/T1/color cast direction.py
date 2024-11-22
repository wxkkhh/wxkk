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

def calculate_green_or_blue_cast(image):
    """
    判断图片是否偏绿色或偏蓝色。
    """
    # 将图像转换为 numpy 数组
    image_np = np.array(image)
    
    # 转换为 Lab 色彩空间
    lab_image = rgb2lab(image_np / 255.0)  # RGB to Lab, scale to [0, 1]
    
    # 获取 Lab 图像的 A 和 B 分量
    A = lab_image[:, :, 1]
    B = lab_image[:, :, 2]
    
    # 计算 A 和 B 的均值
    avg_A = np.mean(A)
    avg_B = np.mean(B)
    
    # 判断偏色方向
    if avg_A < 0:
        return "偏绿色"
    elif avg_B < 0:
        return "偏蓝色"
    else:
        return "无明显偏绿色或偏蓝色"

def main(image_path):
    # 将图像转换为 24 位 RGB 格式
    image = convert_to_24bpp_rgb(image_path)
    
    # 检测偏色方向
    color_cast = calculate_green_or_blue_cast(image)
    
    print(f"Color Cast: {color_cast}")
    return color_cast

# 示例用法
image_path = "d:\GitHub\wxkk\python\\pexel2.jpg"  # 替换为实际图片路径
main(image_path)
