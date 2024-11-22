import cv2

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
    is_blurry = laplacian_var < threshold
    return is_blurry, laplacian_var

# 测试代码
image_path = "d:\GitHub\wxkk\python\\image_160.png"  # 替换为你的图像路径
is_blurry, laplacian_var = detect_blur(image_path)

if is_blurry:
    print(f"The image is blurry. (Variance: {laplacian_var:.2f})")
else:
    print(f"The image is clear. (Variance: {laplacian_var:.2f})")
