import os
import sys
import time
import zipfile

# 获取当前脚本所在的目录（即 OpenJLC/workspace）
workspace_dir = os.path.dirname(os.path.abspath(__file__))

# 定义 Gerber 文件夹路径
gerber_dir = os.path.join(workspace_dir, 'Gerber')

# 1. 判断文件夹是否为空
if not os.listdir(gerber_dir):
    print("File Not Found.")
    time.sleep(3)
    sys.exit()

# 2. 检查是否存在 .zip 文件
zip_files = [f for f in os.listdir(gerber_dir) if f.endswith('.zip')]

if not zip_files:
    # 5. 如果没有 .zip 文件则跳过解压
    print("No .zip files found.")
    time.sleep(3)
    sys.exit()

# 3. 判断存在几个 .zip 文件
if len(zip_files) > 1:
    print("Not specified.")
    time.sleep(3)
    sys.exit()

# 4. 如果只有一个 .zip 文件，解压它
zip_file_path = os.path.join(gerber_dir, zip_files[0])

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(gerber_dir)

# 删除 .zip 文件
os.remove(zip_file_path)

print(f"Unzipped and removed: {zip_files[0]}")

# 6. 延时3秒
time.sleep(3)
