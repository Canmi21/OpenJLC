import os
import sys
import shutil
import subprocess
import time
import yaml
from datetime import datetime

def log_message(message, log_file_path):
    current_time = datetime.now().strftime('%H:%M:%S')
    log_entry = f"{current_time} {message}"
    print(log_entry)  # 输出到终端
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry + '\n')
        log_file.flush()  # 确保每次写入后立即刷新

def main():
    # 获取OpenJLC路径
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

    # 记录日志开始
    log_message("[todo.py] XC Logs start collecting.", log_file_path)

    log_message(f"OpenJLC path: {openjlc_dir}", log_file_path)

    # 定义init.py的路径
    init_script = os.path.join(openjlc_dir, 'init.py')
    if os.path.exists(init_script):
        try:
            subprocess.run(['python', init_script], check=True)
            log_message(f"Init script executed successfully.", log_file_path)
        except subprocess.CalledProcessError as e:
            log_message(f"Error executing init script: {e}", log_file_path)
            sys.exit(1)
    else:
        log_message(f"Error: {init_script} not found.", log_file_path)
        sys.exit(1)

    # 延时0.5秒
    #time.sleep(0.5)

    # 定义PCB下单必读.txt的路径
    output_file = os.path.join(openjlc_dir, 'output', 'PCB下单必读.txt')
    gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')

    log_message(f"Looking for file: {output_file}", log_file_path)
    if os.path.exists(output_file):
        try:
            shutil.copy2(output_file, gerber_dir)
            log_message(f"Copied {output_file} to {gerber_dir}", log_file_path)
        except Exception as e:
            log_message(f"Error copying file: {e}", log_file_path)
            sys.exit(1)
    else:
        log_message(f"Error: {output_file} not found.", log_file_path)
        sys.exit(1)

    # 延时0.5秒
    #time.sleep(0.5)

    # 打开identification.py并执行
    identification_script = os.path.join(openjlc_dir, 'workspace', 'identification.py')
    if os.path.exists(identification_script):
        try:
            subprocess.run(['python', identification_script], check=True)
            log_message(f"Identification script executed successfully.", log_file_path)
        except subprocess.CalledProcessError as e:
            log_message(f"Error executing identification script: {e}", log_file_path)
            sys.exit(1)
    else:
        log_message(f"Error: {identification_script} not found.", log_file_path)
        sys.exit(1)

    log_message("Todo script completed.", log_file_path)

    # 记录日志结束
    log_message("[todo.py] XC Logs done.", log_file_path)

    # 停止日志写入，恢复标准输出
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
