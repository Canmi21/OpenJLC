import os
import sys
import shutil
import subprocess
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
        log_message("Error: OpenJLC environment variable is not set.", log_file_path)
        sys.exit(1)

    log_message(f"OpenJLC path: {openjlc_dir}", log_file_path)

    # 检查传入的.zip文件路径
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.zip'):
        log_message("Usage: reg.py <zip_file_path>", log_file_path)
        sys.exit(1)

    zip_file_path = sys.argv[1]
    log_message(f"ZIP file path: {zip_file_path}", log_file_path)

    # 生成package.yaml报告，尽可能提前执行
    package_report_path = os.path.join(openjlc_dir, 'workspace', 'package.yaml')

    # 删除旧的package.yaml文件（如果存在）
    if os.path.exists(package_report_path):
        try:
            os.remove(package_report_path)
            log_message(f"Deleted old package report: {package_report_path}", log_file_path)
        except Exception as e:
            log_message(f"Error deleting old package report: {e}", log_file_path)
            sys.exit(1)

    # 定义报告内容
    package_report_content = {
        'original': os.path.dirname(zip_file_path).replace("\\", "/") + "/",
        'name': os.path.basename(zip_file_path),  # 使用.zip文件的原始名称
        'logs': log_file_path  # 将日志文件路径添加到package.yaml
    }

    try:
        with open(package_report_path, 'w', encoding='utf-8') as report_file:
            yaml.dump(package_report_content, report_file, default_flow_style=False, allow_unicode=True)
        log_message(f"Package report generated at {package_report_path}", log_file_path)
    except Exception as e:
        log_message(f"Error generating package report: {e}", log_file_path)
        sys.exit(1)

    # 定义Gerber目录
    gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')

    # 确保目标文件夹存在
    if not os.path.exists(gerber_dir):
        os.makedirs(gerber_dir)
    log_message(f"Gerber directory: {gerber_dir}", log_file_path)

    # 清空Gerber目录中的所有文件
    try:
        for filename in os.listdir(gerber_dir):
            file_path = os.path.join(gerber_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 删除文件或符号链接
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 删除目录
        log_message(f"Cleared Gerber directory: {gerber_dir}", log_file_path)
    except Exception as e:
        log_message(f"Error clearing Gerber directory: {e}", log_file_path)
        sys.exit(1)

    # 复制选中的.zip文件到Gerber目录
    destination = os.path.join(gerber_dir, os.path.basename(zip_file_path))
    try:
        shutil.copy2(zip_file_path, destination)
        log_message(f"Copied {zip_file_path} to {destination}", log_file_path)
    except Exception as e:
        log_message(f"Error copying file: {e}", log_file_path)
        sys.exit(1)

    # 执行unzip.py脚本
    unzip_script = os.path.join(openjlc_dir, 'workspace', 'unzip.py')
    if os.path.exists(unzip_script):
        try:
            subprocess.run(['python', unzip_script], check=True)
            log_message("Unzip script executed successfully.", log_file_path)
        except subprocess.CalledProcessError as e:
            log_message(f"Error executing unzip script: {e}", log_file_path)
            sys.exit(1)
    else:
        log_message(f"Error: {unzip_script} not found.", log_file_path)
        sys.exit(1)

    # 检查 PCB下单必读.txt 是否存在
    pcb_must_read_file = os.path.join(gerber_dir, 'PCB下单必读.txt')
    if os.path.exists(pcb_must_read_file):
        log_message("Already LCEDA File.", log_file_path)

        # 执行clear.py脚本
        clear_script_path = os.path.join(openjlc_dir, 'workspace', 'clear.py')
        if os.path.exists(clear_script_path):
            try:
                subprocess.run(['python', clear_script_path], check=True)
                log_message("Clear script executed successfully.", log_file_path)
            except subprocess.CalledProcessError as e:
                log_message(f"Error executing clear script: {e}", log_file_path)
                sys.exit(1)
        else:
            log_message(f"Clear script {clear_script_path} not found.", log_file_path)

        log_message("[Reg.py] XC Logs done.", log_file_path)
        sys.stdout = sys.__stdout__  # 恢复标准输出流，停止日志写入
        sys.exit(0)  # 退出程序，不执行todo.py

    else:
        log_message(f"{pcb_must_read_file} not found, proceeding with todo.py execution.", log_file_path)

    # 执行todo.py脚本
    todo_script = os.path.join(openjlc_dir, 'workspace', 'todo.py')
    if os.path.exists(todo_script):
        try:
            log_message("[Reg.py] XC Logs done.", log_file_path)
            sys.stdout = sys.__stdout__  # 恢复标准输出流，停止日志写入
            subprocess.run(['python', todo_script], check=True)
            print("Todo script executed successfully.")
        except subprocess.CalledProcessError as e:
            log_message(f"Error executing todo script: {e}", log_file_path)
            sys.exit(1)
    else:
        log_message(f"Error: {todo_script} not found.", log_file_path)
        sys.exit(1)

if __name__ == "__main__":
    # 创建日志文件路径
    logs_dir = os.path.join(os.environ.get("OpenJLC"), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_filename = datetime.now().strftime('%Y-%m-%d-%H-%M') + '.log'
    log_file_path = os.path.join(logs_dir, log_filename)

    # 打开日志文件并重定向stdout和stderr
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        sys.stdout = log_file
        sys.stderr = log_file

        log_message("[Reg.py] XC Logs start collecting.", log_file_path)
        main()
