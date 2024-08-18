import os
from datetime import datetime
import random
import sys
import yaml

def log_message(message, log_file_path):
    current_time = datetime.now().strftime('%H:%M:%S')
    log_entry = f"{current_time} {message}"
    print(log_entry)  # 输出到终端
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry + '\n')
        log_file.flush()  # 确保每次写入后立即刷新

def main():
    # 获取OpenJLC环境变量
    openjlc_dir = os.environ.get("OpenJLC")
    if not openjlc_dir:
        print("Error: OpenJLC environment variable is not set.")
        sys.exit(1)

    # 读取package.yaml文件中的日志文件路径
    package_yaml_path = os.path.join(openjlc_dir, 'workspace', 'package.yaml')
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
    log_file_path = os.path.join(openjlc_dir, 'logs', log_filename)

    # 记录初始化日志开始
    log_message("[init.py] XC Logs start collecting.", log_file_path)

    # 定义要创建的文件夹和文件路径
    output_dir = os.path.join(openjlc_dir, 'output')
    output_file = os.path.join(output_dir, 'PCB下单必读.txt')

    config_dir = os.path.join(openjlc_dir, 'config')
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

    log_message(f"done(1/2).: {output_file}", log_file_path)

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

    log_message(f"done(2/2).: {header_file}", log_file_path)

    # 记录初始化日志结束
    log_message("[init.py] XC Logs done.", log_file_path)

    # 停止日志写入，恢复标准输出
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
