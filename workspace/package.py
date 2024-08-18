import os
import shutil
import time
import zipfile
import yaml
import subprocess
from datetime import datetime
import sys

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
        return

    # 读取package.yaml文件中的日志文件路径
    package_yaml_path = os.path.join(openjlc_dir, 'workspace', 'package.yaml')
    if not os.path.exists(package_yaml_path):
        print("Error: package.yaml not found.")
        return

    with open(package_yaml_path, 'r', encoding='utf-8') as package_file:
        package_data = yaml.safe_load(package_file)
        log_filename = package_data.get('logs')
        if not log_filename:
            print("Error: 'logs' field not found in package.yaml.")
            return

    # 设置日志文件路径
    log_file_path = os.path.join(openjlc_dir, 'logs', log_filename)

    # 记录package.py日志开始
    log_message("[package.py] XC Logs start collecting.", log_file_path)

    # 定义工作流目录和文件路径
    workflow_dir = os.path.join(openjlc_dir, 'workspace', 'workflow')
    gerber_file = os.path.join(openjlc_dir, 'workspace', 'Gerber', 'PCB下单必读.txt')
    report_file = os.path.join(openjlc_dir, 'workspace', 'report.yaml')

    # 等待0.3秒
    time.sleep(0.3)

    # 确保工作流目录存在
    if not os.path.exists(workflow_dir):
        log_message(f"Workflow directory {workflow_dir} does not exist.", log_file_path)
        return

    # 复制PCB下单必读.txt到workflow目录
    if os.path.exists(gerber_file):
        shutil.copy2(gerber_file, workflow_dir)
        log_message(f"Copied {gerber_file} to {workflow_dir}", log_file_path)
    else:
        log_message(f"{gerber_file} does not exist.", log_file_path)
        return

    # 读取report.yaml文件
    if os.path.exists(report_file):
        with open(report_file, 'r', encoding='utf-8') as f:
            report_data = yaml.safe_load(f)
    else:
        log_message(f"{report_file} does not exist.", log_file_path)
        return

    # 根据Source字段确定名字
    source = report_data.get('Source', 'Unknown')
    if source == 'LCEDA':
        name_str = "LC"
    elif source == 'AD':
        name_str = "AD"
    elif source == 'KiCAD':
        name_str = "Ki"
    else:
        name_str = "Err"

    # 打包workflow目录下的所有文件到package.zip
    package_zip = os.path.join(openjlc_dir, 'workspace', 'package.zip')
    with zipfile.ZipFile(package_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(workflow_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), workflow_dir))
    log_message(f"Packaged files into {package_zip}", log_file_path)

    # 读取package.yaml文件
    if os.path.exists(package_yaml_path):
        with open(package_yaml_path, 'r', encoding='utf-8') as f:
            package_data = yaml.safe_load(f)
    else:
        log_message(f"{package_yaml_path} does not exist.", log_file_path)
        return

    # 计算层数和生成新的文件名
    layers = sum(1 for key in ['Top_Cu', 'Bottom_Cu', 'InnerLayer1_Cu', 'InnerLayer2_Cu', 'InnerLayer3_Cu', 'InnerLayer4_Cu'] if report_data.get(key) == 'Yes')
    if layers == 1:
        layer_str = "L1"
    elif layers == 2:
        layer_str = "L2"
    elif layers in [4, 6]:
        layer_str = f"L{layers}"
    else:
        layer_str = "Err"

    # 修改文件名
    base_name = os.path.splitext(package_data['name'])[0]
    new_package_name = f"{base_name}-{name_str}-{layer_str}.zip"
    new_package_path = os.path.join(openjlc_dir, 'workspace', new_package_name)

    # 重命名并复制文件
    os.rename(package_zip, new_package_path)
    log_message(f"Package renamed to {new_package_name}", log_file_path)

    destination_path = os.path.join(package_data['original'], new_package_name)
    shutil.copy2(new_package_path, destination_path)
    log_message(f"Copied {new_package_name} to {package_data['original']}", log_file_path)

    # 删除workspace中的package.zip
    os.remove(new_package_path)
    log_message(f"Deleted {new_package_name} from workspace.", log_file_path)

    # 记录package.py日志结束
    log_message("[package.py] XC Logs done.", log_file_path)
    sys.stdout = sys.__stdout__  # 恢复标准输出

    # 执行clear.py脚本
    clear_script_path = os.path.join(openjlc_dir, 'workspace', 'clear.py')
    if os.path.exists(clear_script_path):
        try:
            subprocess.run(['python', clear_script_path], check=True)
            print(f"Clear script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing clear script: {e}")
    else:
        print(f"Clear script {clear_script_path} not found.")

if __name__ == "__main__":
    main()
