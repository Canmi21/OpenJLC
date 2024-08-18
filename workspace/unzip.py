import os
import sys
import time
import zipfile
from datetime import datetime
import yaml

def log_message(message, log_file_path):
    current_time = datetime.now().strftime('%H:%M:%S')
    log_entry = f"{current_time} {message}"
    print(log_entry)  # 输出到终端
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry + '\n')
        log_file.flush()  # 确保每次写入后立即刷新

def main():
    # 获取当前脚本所在的目录（即 OpenJLC/workspace）
    workspace_dir = os.path.dirname(os.path.abspath(__file__))

    # 读取 package.yaml 文件中的日志文件路径
    package_yaml_path = os.path.join(workspace_dir, 'package.yaml')
    if not os.path.exists(package_yaml_path):
        print("Error: package.yaml not found.")
        sys.exit(1)

    with open(package_yaml_path, 'r', encoding='utf-8') as package_file:
        package_data = yaml.safe_load(package_file)
        log_filename = package_data.get('logs')
        if not log_filename:
            print("Error: 'logs' field not found in package.yaml.")
            sys.exit(1)

    # 设置日志文件路径
    log_file_path = os.path.join(os.path.dirname(workspace_dir), 'logs', log_filename)

    # 记录日志开始
    log_message("[unzip.py] XC Logs start collecting.", log_file_path)

    # 定义 Gerber 文件夹路径
    gerber_dir = os.path.join(workspace_dir, 'Gerber')

    # 1. 判断文件夹是否为空
    if not os.listdir(gerber_dir):
        log_message("File Not Found.", log_file_path)
        time.sleep(3)
        sys.exit()

    # 2. 检查是否存在 .zip 文件
    zip_files = [f for f in os.listdir(gerber_dir) if f.endswith('.zip')]

    if not zip_files:
        # 5. 如果没有 .zip 文件则跳过解压
        log_message("No .zip files found.", log_file_path)
        time.sleep(3)
        sys.exit()

    # 3. 判断存在几个 .zip 文件
    if len(zip_files) > 1:
        log_message("Not specified.", log_file_path)
        time.sleep(3)
        sys.exit()

    # 4. 如果只有一个 .zip 文件，解压它
    zip_file_path = os.path.join(gerber_dir, zip_files[0])

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(gerber_dir)

    # 删除 .zip 文件
    os.remove(zip_file_path)

    log_message(f"Unzipped and removed: {zip_files[0]}", log_file_path)

    # 记录日志结束
    log_message("[unzip.py] XC Logs done.", log_file_path)

    # 停止日志写入，恢复标准输出
    sys.stdout = sys.__stdout__

    # 延时
    # time.sleep(0.5)

if __name__ == "__main__":
    main()
