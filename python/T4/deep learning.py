import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import convolve
from sklearn.preprocessing import MinMaxScaler
import math
import pandas as pd
from skimage.color import rgb2lab
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image

# 全局定义深度变量，方便统一调整
GLOBAL_DEPTH = [1.0, 5.0, 10.0]  # 可以定义多个深度值，便于计算和对比

# 创建增强后的图像保存文件夹
os.makedirs('enhanced', exist_ok=True)

# 定义数据集类，使用 EUVP 数据集
class EUVPDataset(Dataset):
    def __init__(self, input_dir, target_dir, transform=None):
        self.input_dir = input_dir
        self.target_dir = target_dir
        self.input_images = os.listdir(input_dir)
        self.transform = transform

    def __len__(self):
        return len(self.input_images)

    def __getitem__(self, idx):
        input_image_path = os.path.join(self.input_dir, self.input_images[idx])
        target_image_path = os.path.join(self.target_dir, self.input_images[idx])

        # 读取输入图像和目标图像
        input_image = Image.open(input_image_path).convert("RGB")
        target_image = Image.open(target_image_path).convert("RGB")

        # 应用变换
        if self.transform:
            input_image = self.transform(input_image)
            target_image = self.transform(target_image)

        return input_image, target_image

# 图像预处理和数据增强
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 数据集路径
input_image_paths = "EUVP/trainA/"
target_image_paths = "EUVP/trainB/"

# 加载数据集
train_dataset = EUVPDataset(input_dir=input_image_paths, target_dir=target_image_paths, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=4)

# 生成器模型定义
class GeneratorUNet(nn.Module):
    def __init__(self, input_channels=3, output_channels=3):
        super(GeneratorUNet, self).__init__()
        self.down1 = self.contracting_block(input_channels, 64)
        self.down2 = self.contracting_block(64, 128)
        self.down3 = self.contracting_block(128, 256)
        self.down4 = self.contracting_block(256, 512)
        
        self.middle = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.ReLU()
        )
        
        self.up4 = self.expansive_block(512, 256)
        self.up3 = self.expansive_block(256, 128)
        self.up2 = self.expansive_block(128, 64)
        self.up1 = nn.Conv2d(64, output_channels, kernel_size=1)

    def contracting_block(self, in_channels, out_channels):
        block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(out_channels)
        )
        return block

    def expansive_block(self, in_channels, out_channels):
        block = nn.Sequential(
            nn.ConvTranspose2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(out_channels)
        )
        return block

    def forward(self, x):
        down1 = self.down1(x)
        down2 = self.down2(down1)
        down3 = self.down3(down2)
        down4 = self.down4(down3)
        middle = self.middle(down4)
        up4 = self.up4(middle)
        up3 = self.up3(up4)
        up2 = self.up2(up3)
        up1 = self.up1(up2)
        return torch.tanh(up1)

# 判别器模型定义
class Discriminator(nn.Module):
    def __init__(self, input_channels=6):  # input_channels includes input and target images
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(input_channels, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            nn.Conv2d(128, 256, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2),
            nn.Conv2d(256, 512, kernel_size=4, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2),
            nn.Conv2d(512, 1, kernel_size=4, stride=1, padding=1)
        )

    def forward(self, input, target):
        x = torch.cat((input, target), dim=1)
        return self.model(x)

# 初始化模型、损失函数、优化器
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
generator = GeneratorUNet().to(device)
discriminator = Discriminator().to(device)

criterion_gan = nn.BCEWithLogitsLoss()
criterion_l1 = nn.L1Loss()

optimizer_g = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
optimizer_d = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

# 训练循环
num_epochs = 100
for epoch in range(num_epochs):
    for i, (input_image, target_image) in enumerate(train_loader):
        input_image, target_image = input_image.to(device), target_image.to(device)
        
        # 判别器训练
        optimizer_d.zero_grad()
        fake_image = generator(input_image).detach()
        real_output = discriminator(input_image, target_image)
        fake_output = discriminator(input_image, fake_image)
        real_loss = criterion_gan(real_output, torch.ones_like(real_output))
        fake_loss = criterion_gan(fake_output, torch.zeros_like(fake_output))
        d_loss = (real_loss + fake_loss) / 2
        d_loss.backward()
        optimizer_d.step()

        # 生成器训练
        optimizer_g.zero_grad()
        fake_image = generator(input_image)
        fake_output = discriminator(input_image, fake_image)
        g_gan_loss = criterion_gan(fake_output, torch.ones_like(fake_output))
        g_l1_loss = criterion_l1(fake_image, target_image)
        g_loss = g_gan_loss + 100 * g_l1_loss
        g_loss.backward()
        optimizer_g.step()

    print(f"Epoch [{epoch+1}/{num_epochs}], D Loss: {d_loss.item():.4f}, G Loss: {g_loss.item():.4f}")

print("训练完成")

# 保存模型
torch.save(generator.state_dict(), "generator_euvp.pth")
torch.save(discriminator.state_dict(), "discriminator_euvp.pth")

# 使用训练好的模型进行推理
generator.eval()
input_image = Image.open("EUVP/testA/image_001.jpg").convert("RGB")
input_tensor = transform(input_image).unsqueeze(0).to(device)

with torch.no_grad():
    restored_tensor = generator(input_tensor)
restored_image = restored_tensor.squeeze().cpu().numpy().transpose(1, 2, 0)
restored_image = (restored_image * 255).astype(np.uint8)

# 保存复原图像
restored_image_pil = Image.fromarray(restored_image)
restored_image_pil.save("restored_image.jpg")
