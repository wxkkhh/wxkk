import numpy as np
import matplotlib.pyplot as plt

def estimate_beta_and_background(depth, I_surface, I_depth):
    """
    根据水下深度计算光衰减系数和背景光强度。
    
    参数:
        depth: 水深 (米)。
        I_surface: 水面光强度 (R, G, B)。
        I_depth: 水下当前光强度 (R, G, B)。
    
    返回:
        beta: 光衰减系数 (R, G, B)。
        B: 背景光强度 (R, G, B)。
    """
    # 确保输入为 numpy 数组
    I_surface = np.array(I_surface)
    I_depth = np.array(I_depth)
    
    # 计算光衰减系数 beta
    beta = -np.log(I_depth / I_surface) / depth
    
    # 背景光强度近似为深度光强
    B = I_depth
    
    return beta, B

# 示例数据
depth = 10  # 水深 10 米
I_surface = [1.0, 1.0, 1.0]  # 假设水面光强为 1（归一化）
I_depth = [0.002, 0.005, 0.007]  # 假设 10 米深度处的光强

# 计算光衰减系数和背景光强度
beta, background_light = estimate_beta_and_background(depth, I_surface, I_depth)

# 显示结果
print(f"光衰减系数 (beta): {beta}")
print(f"背景光强度 (B): {background_light}")

# 可视化光衰减
colors = ['Red', 'Green', 'Blue']
plt.bar(colors, beta, color=['red', 'green', 'blue'])
plt.title("光衰减系数 (Beta)")
plt.ylabel("Beta")
plt.show()

plt.bar(colors, background_light, color=['red', 'green', 'blue'])
plt.title("背景光强度 (Background Light)")
plt.ylabel("Intensity")
plt.show()
