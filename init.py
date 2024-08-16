import os
from datetime import datetime
import random

# 定义要创建的文件夹和文件路径
output_dir = os.path.join(os.getcwd(), 'output')
output_file = os.path.join(output_dir, 'PCB下单必读.txt')

config_dir = os.path.join(os.getcwd(), 'config')
header_file = os.path.join(config_dir, 'Header.yaml')

# 检查是否存在output文件夹，如果不存在则创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 创建PCB下单必读.txt的文件内容
pcb_content = """如何进行PCB下单

请查看：
https://docs.lceda.cn/cn/PCB/Order-PCB"""

# 创建文件并写入内容
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(pcb_content)

print(f"done(1/2).: {output_file}")

# 检查是否存在config文件夹，如果不存在则创建
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

# 获取当前时间
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 生成随机版本号
major_version = random.randint(1, 2)
if major_version == 1:
    minor_version = 9
    patch_version = 28
    build_version = ""
else:
    minor_version = random.randint(0, 2)
    patch_version = 22
    build_version = f".{random.randint(0, 5)}"

version = f"v{major_version}.{minor_version}.{patch_version}{build_version}"

# 创建Header.yaml的文件内容
header_content = f"""Header: |-
  G04 EasyEDA Pro {version}, {current_time}*
  G04 Gerber Generator version 0.3*"""

# 创建Header.yaml文件并写入内容
with open(header_file, 'w', encoding='utf-8') as file:
    file.write(header_content)

print(f"done(2/2).: {header_file}")
