import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import convolve
from sklearn.preprocessing import MinMaxScaler
import math
import pandas as pd
from skimage.color import rgb2lab

# 全局定义深度变量，方便统一调整
GLOBAL_DEPTH = [1.0, 5.0, 10.0]  # 可以定义多个深度值，便于计算和对比

# 创建增强后的图像保存文件夹
os.makedirs('enhanced', exist_ok=True)

# 颜色偏差复原方案
def restore_color_cast(image):
    # 使用白平衡算法进行颜色校正
    result = cv2.xphoto.createSimpleWB().balanceWhite(image)
    return result

# 光线不足复原方案
def restore_low_light(image):
    # 使用 CLAHE（自适应直方图均衡化）增强亮度
    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    lab_image[:, :, 0] = clahe.apply(lab_image[:, :, 0])
    restored_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2RGB)
    return restored_image

# 模糊复原方案（使用去雾算法）
def restore_blur(image):
    # 使用暗通道先验去雾算法进行模糊复原
    def get_dark_channel(image, size=15):
        min_channel = np.amin(image, axis=2).astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
        dark_channel = cv2.erode(min_channel, kernel)
        return dark_channel

    def get_atmospheric_light(image, dark_channel):
        num_pixels = dark_channel.size
        num_brightest = int(max(num_pixels * 0.001, 1))
        flat_dark = dark_channel.flatten()
        flat_image = image.reshape((-1, 3))
        indices = np.argpartition(flat_dark, -num_brightest)[-num_brightest:]
        atmospheric_light = np.mean(flat_image[indices], axis=0)
        return atmospheric_light

    def get_transmission_estimate(image, atmospheric_light, omega=0.95, size=15):
        norm_image = image / (atmospheric_light + 1e-6)
        transmission = 1 - omega * get_dark_channel(norm_image, size)
        return transmission.astype(np.float32)

    def get_transmission_refine(image, transmission, radius=60):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
        transmission_refined = cv2.ximgproc.guidedFilter(guide=gray, src=transmission, radius=radius, eps=1e-3)
        return transmission_refined

    def recover(image, transmission, atmospheric_light, t0=0.1):
        transmission = np.clip(transmission, t0, 1)[:, :, None]
        recovered_image = (image - atmospheric_light) / transmission + atmospheric_light
        recovered_image = np.clip(recovered_image, 0, 255).astype(np.uint8)
        return recovered_image

    dark_channel = get_dark_channel(image)
    atmospheric_light = get_atmospheric_light(image, dark_channel)
    transmission_estimate = get_transmission_estimate(image, atmospheric_light)
    transmission_refined = get_transmission_refine(image, transmission_estimate)
    restored_image = recover(image, transmission_refined, atmospheric_light)
    return restored_image

# 偏色检测函数，使用 CIE Lab 色彩空间计算偏色因子 K
def detect_color_cast(image):
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

# 简单分类函数并归一化处理
def classify_image(image, scaler):
    # 计算灰度直方图并判断亮度是否不足
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    hist, bins = np.histogram(gray_image.ravel(), bins=256, range=(0, 256))
    low_brightness_pixels = np.sum(hist[:50])  # 灰度值小于 50 的像素数量
    total_pixels = gray_image.size
    low_brightness_ratio = low_brightness_pixels / total_pixels

    # 计算图像的拉普拉斯方差（清晰度）
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()

    # 计算偏色因子 K
    color_cast_factor = detect_color_cast(image)

    # 将特征归一化
    features = np.array([low_brightness_ratio, laplacian_var, color_cast_factor]).reshape(1, -1)
    normalized_features = scaler.transform(features)[0]
    normalized_brightness_ratio, normalized_laplacian, normalized_color_cast = normalized_features

    # 识别最严重的问题类别
    severity_scores = {
        'low_light': normalized_brightness_ratio,
        'blur': 1 - normalized_laplacian,  # 值越高表示模糊越严重
        'color_cast': normalized_color_cast
    }
    most_severe_category = max(severity_scores, key=severity_scores.get)
    return most_severe_category

# 计算 PSNR
def calculate_psnr(original, restored):
    mse = np.mean((original - restored) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

# 计算 UCIQE（用于水下图像质量评估的指标）
def calculate_uciqe(image):
    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    L = lab_image[:, :, 0].flatten() / 255.0
    A = lab_image[:, :, 1].flatten()
    B = lab_image[:, :, 2].flatten()
    C_ab = np.sqrt(A ** 2 + B ** 2)
    uciqe = 0.4680 * np.std(L) + 0.2745 * np.mean(C_ab) + 0.2576 * (np.percentile(L, 99) - np.percentile(L, 1))
    return uciqe

# 计算 UIQM（水下图像质量指标）
def calculate_uiqm(image):
    b, g, r = cv2.split(image)
    r_mean, g_mean, b_mean = np.mean(r), np.mean(g), np.mean(b)
    r_contrast, g_contrast, b_contrast = np.std(r), np.std(g), np.std(b)
    r_saturation, g_saturation, b_saturation = np.mean(r / (g + 1e-10)), np.mean(g / (b + 1e-10)), np.mean(b / (r + 1e-10))
    uiqm = 0.0282 * (r_mean + g_mean + b_mean) + 0.2953 * (r_contrast + g_contrast + b_contrast) + 0.3654 * (r_saturation + g_saturation + b_saturation)
    return uiqm

# 初始化归一化器
scaler = MinMaxScaler()

# 收集所有图像的特征以进行归一化训练
feature_list = []
input_folder = 'D:\\2024 APMCM Problem A\\Attachment 2'  # 替换为你的图像文件夹路径
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        hist, bins = np.histogram(gray_image.ravel(), bins=256, range=(0, 256))
        low_brightness_pixels = np.sum(hist[:50])  # 灰度值小于 50 的像素数量
        total_pixels = gray_image.size
        low_brightness_ratio = low_brightness_pixels / total_pixels
        laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
        color_cast_factor = detect_color_cast(image)
        feature_list.append([low_brightness_ratio, laplacian_var, color_cast_factor])

# 对特征进行归一化训练
scaler.fit(feature_list)

# 批量处理文件夹中的图像
output_folder = 'D:\\2024 APMCM Problem A\\enhanced'
os.makedirs(output_folder, exist_ok=True)

# 创建用于保存指标的列表
results = []

# 遍历文件夹中的所有图像文件
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(input_folder, filename)
        input_image = cv2.imread(image_path)
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        # 分类图像类型
        image_category = classify_image(input_image, scaler)

        # 根据分类结果应用相应的复原方法
        if image_category == 'low_light':
            restored_image = restore_low_light(input_image)
        elif image_category == 'blur':
            restored_image = restore_blur(input_image)
        elif image_category == 'color_cast':
            restored_image = restore_color_cast(input_image)
        else:
            restored_image = input_image

        # 保存复原后的图像
        restored_image_path = os.path.join(output_folder, f'restored_{filename}')
        cv2.imwrite(restored_image_path, cv2.cvtColor(restored_image, cv2.COLOR_RGB2BGR))

        # 计算 PSNR, UCIQE, UIQM
        psnr = calculate_psnr(input_image, restored_image)
        uciqe = calculate_uciqe(restored_image)
        uiqm = calculate_uiqm(restored_image)

        # 保存指标结果
        results.append([filename, image_category, psnr, uciqe, uiqm])

# 创建 DataFrame 并保存为 Excel 文件
df = pd.DataFrame(results, columns=['Image Filename', 'Category', 'PSNR', 'UCIQE', 'UIQM'])
output_excel_path = 'D:\\2024 APMCM Problem A\\enhanced/image_quality_metrics.xlsx'
df.to_excel(output_excel_path, index=False)
print(f'指标结果已保存到 {output_excel_path}')

# 显示最后处理的图像作为示例
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Input Image")
plt.imshow(input_image)
plt.subplot(1, 2, 2)
plt.title("Restored Image")
plt.imshow(restored_image)
plt.show()
