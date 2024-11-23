import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.color import rgb2lab
import pandas as pd

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.color import rgb2lab
import pandas as pd


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
    is_low_brightness = low_brightness_ratio_actual 
    
    # 绘制灰度图和直方图
    # plt.figure(figsize=(12, 6))
    
    # 显示灰度图像
    # plt.subplot(1, 2, 1)
    # plt.imshow(image, cmap='gray')
    # plt.title("Gray Image")
    # plt.axis("off")
    
    # 绘制灰度直方图
    # plt.subplot(1, 2, 2)
    # plt.bar(bins[:-1], hist, width=1, color='gray', edgecolor='black')
    # plt.title("Gray Level Distribution")
    # plt.xlabel("Gray Level")
    # plt.ylabel("Pixel Count")
    # plt.axvline(x=brightness_threshold, color='red', linestyle='--', label='Brightness Threshold')
    # plt.legend()
    
    # plt.tight_layout()
    # plt.show()
    
    # 打印检测结果
    # print(f"低亮度像素比例: {low_brightness_ratio_actual:.2%}")
    # print(f"是否亮度不足: {'是' if is_low_brightness else '否'}")
    
    return is_low_brightness

def detect_blur(image_path, threshold=100):
    """
    检测图像是否模糊
    :param image_path: 图像文件路径
    :param threshold: 判断模糊的阈值，默认值为100
    :return: True（模糊），False（清晰），以及拉普拉斯方差值
    """
    # 读取图像并转为灰度图
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to read.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 计算拉普拉斯变换
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # 判断是否模糊
    if laplacian_var < threshold:
        blurry = (threshold - laplacian_var) / threshold
    else:
        blurry = 0.0
    print(blurry)
    return blurry

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
    val = (10-color_cast_factor)/color_cast_factor
    return val

def main(image_path):
    # 将图像转换为 24 位 RGB 格式
    image = convert_to_24bpp_rgb(image_path)
    
    # 计算偏色因子
    color_cast_factor = calculate_color_cast(image)
    color_cast_type = calculate_green_or_blue_cast(image)
    if color_cast_factor > 4:
        val = (color_cast_factor-4)/4
    else:
        val = color_cast_factor / 4
    # print(color_cast_factor)
    return val

# 示例用法
# image_path = "d:\GitHub\wxkk\python\\pexel2.jpg"  # 替换为你的图像路径
# low_bright_chk = detect_low_brightness(image_path)
# blurry_chk, laplacian_var_chk = detect_blur(image_path)
# color_cast_factor, color_cast_type = main(image_path)
# #print({low_bright_chk, blurry_chk, laplacian_var_chk, color_cast_factor, color_cast_type})
# print(low_bright_chk)
# print(blurry_chk)
# print(laplacian_var_chk)
# print(color_cast_factor)
# print(color_cast_type)

def choose_type(image_path):
  low_bright_chk = detect_low_brightness(image_path)
  blurry_chk = detect_blur(image_path)
  color_cast_factor = main(image_path)
  all_type = ["low light", "blur", "color cast"]
  # color_cast_factor = 1
  # print(low_bright_chk, blurry_chk, color_cast_factor)
  if low_bright_chk > blurry_chk and low_bright_chk > color_cast_factor:
      return "low light"
  elif blurry_chk > low_bright_chk and blurry_chk > color_cast_factor:
      return "blur"
  else:
      return "color cast"
  

image_path1 = [f"D:\\2024 APMCM Problem A\\Attachment 1\\image_{str(i).zfill(3)}.png" for i in range(1, 272)]
# print(image_path[1])
image_path2 = [f"D:\\2024 APMCM Problem A\\Attachment 1\\image_{str(i).zfill(3)}.jpg" for i in range(273, 400)]
image_categories = []
for i in range(0, 271):
    get_type = choose_type(image_path1[i])
    image_categories.append(get_type)
    print(image_path1[i], get_type)

for i in range(273, 400):
    get_type = choose_type(image_path2[i-273])
    image_categories.append(get_type)
    print(image_path2[i-273], get_type)


# image_categories = choose_type(image_path[i] for i in range(1, 272))
df = pd.DataFrame({
    "Image_Files": image_path1+image_path2,
    "Category": image_categories
})
file_name = "D:\\2024 APMCM Problem A\\Attachment 1\\image_files_with_categories.xlsx"
df.to_excel(file_name, index=False)

print(f"文件已成功保存为 {file_name}")


