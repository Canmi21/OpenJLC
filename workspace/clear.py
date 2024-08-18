import os
import shutil
import sys
from datetime import datetime
import yaml

def log_message(message, log_file_path):
    current_time = datetime.now().strftime('%H:%M:%S')
    log_entry = f"{current_time} {message}"
    print(log_entry)  # 输出到终端
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry + '\n')
        log_file.flush()  # 确保每次写入后立即刷新

def clear_directory(directory, log_file_path):
    try:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            log_message(f"Cleared contents of directory: {directory}", log_file_path)
        else:
            log_message(f"Directory does not exist: {directory}", log_file_path)
    except Exception as e:
        log_message(f"Error clearing directory {directory}: {e}", log_file_path)

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

    # 记录clear.py日志开始
    log_message("[clear.py] XC Logs start collecting.", log_file_path)

    # 定义需要清理的目录
    gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')
    workflow_dir = os.path.join(openjlc_dir, 'workspace', 'workflow')

    # 清理Gerber和workflow目录
    clear_directory(gerber_dir, log_file_path)
    clear_directory(workflow_dir, log_file_path)

    # 记录清理操作完成日志
    log_message("[clear.py] XC Logs done.", log_file_path)

    # 清理残留的package信息
    try:
        os.remove(package_yaml_path)
        log_message(f"Deleted {package_yaml_path} to ensure it is recreated next time.", log_file_path)
    except FileNotFoundError:
        log_message(f"{package_yaml_path} not found, no deletion necessary.", log_file_path)
    except Exception as e:
        log_message(f"Error deleting {package_yaml_path}: {e}", log_file_path)

if __name__ == "__main__":
    main()
