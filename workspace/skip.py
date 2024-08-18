import os
import re
import yaml
import shutil
from datetime import datetime
import subprocess
import sys  # 添加此行以导入 sys 模块

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

    # 记录skip.py日志开始
    log_message("[skip.py] XC Logs start collecting.", log_file_path)

    # 定义Gerber和workflow目录
    gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')
    workflow_dir = os.path.join(openjlc_dir, 'workspace', 'workflow')
    report_file_path = os.path.join(openjlc_dir, 'workspace', 'report.yaml')

    # 清空workflow目录
    if os.path.exists(workflow_dir):
        shutil.rmtree(workflow_dir)
    os.makedirs(workflow_dir)
    log_message(f"Cleared and recreated workflow directory: {workflow_dir}", log_file_path)

    # 复制Gerber目录到workflow目录
    try:
        shutil.copytree(gerber_dir, workflow_dir, dirs_exist_ok=True)
        log_message(f"Copied {gerber_dir} to {workflow_dir}", log_file_path)
    except Exception as e:
        log_message(f"Error copying files: {e}", log_file_path)
        return

    # 检查workflow目录中的文件并生成report.yaml
    report_data = {
        'Date': datetime.now().strftime("%Y-%m-%d"),
        'Time': datetime.now().strftime("%H:%M:%S"),
        'Source': 'LCEDA',  # 修改为 'LCEDA'
        'Outline': 'No',
        'Edge': 'No',
        'Top_Cu': 'No',
        'Bottom_Cu': 'No',
        'InnerLayer1_Cu': 'No',
        'InnerLayer2_Cu': 'No',
        'InnerLayer3_Cu': 'No',
        'InnerLayer4_Cu': 'No',
        'Top_SilkScreen': 'No',
        'Bottom_SilkScreen': 'No',
        'Top_SolderMask': 'No',
        'Bottom_SolderMask': 'No',
        'Top_SolderPaste': 'No',
        'Bottom_SolderPaste': 'No',
        'PTH': 'No',
        'NPTH': 'No',
        'PTH_Via': 'No'
    }

    # 定义文件名和report字段的映射关系
    file_mapping = {
        'Outline': r'\.GKO$|\.gm1$|Edge_Cuts|-Edge_Cuts|\.gm13$',  # 主要处理Outline类文件
        'Top_Cu': r'\.GTL$',
        'Bottom_Cu': r'\.GBL$',
        'InnerLayer1_Cu': r'\.G1$',
        'InnerLayer2_Cu': r'\.G2$',
        'InnerLayer3_Cu': r'\.G3$',
        'InnerLayer4_Cu': r'\.G4$',
        'Top_SilkScreen': r'\.GTO$',
        'Bottom_SilkScreen': r'\.GBO$',
        'Top_SolderMask': r'\.GTS$',
        'Bottom_SolderMask': r'\.GBS$',
        'Top_SolderPaste': r'\.GTP$',
        'Bottom_SolderPaste': r'\.GBP$',
        'PTH': r'\.TXT$',
        'NPTH': r'\.TXT$',
        'PTH_Via': r'\.TXT$'
    }

    # 逐文件检查workflow目录中的文件类型
    for file_name in os.listdir(workflow_dir):
        for key, pattern in file_mapping.items():
            if re.search(pattern, file_name, re.IGNORECASE):
                report_data[key] = 'Yes'
                log_message(f"Matched {key} with file {file_name}", log_file_path)
                break

    # 保存报告到report.yaml
    try:
        with open(report_file_path, 'w', encoding='utf-8') as report_file:
            yaml.dump(report_data, report_file, default_flow_style=False, allow_unicode=True)
        log_message(f"Report generated at {report_file_path}", log_file_path)
    except Exception as e:
        log_message(f"Error writing report: {e}", log_file_path)
        return

    # 读取package.yaml文件，删除源文件
    if os.path.exists(package_yaml_path):
        try:
            with open(package_yaml_path, 'r', encoding='utf-8') as f:
                package_data = yaml.safe_load(f)
                original_file_path = os.path.join(package_data['original'], package_data['name'])

            if os.path.exists(original_file_path):
                os.remove(original_file_path)
                log_message(f"Deleted original file: {original_file_path}", log_file_path)
            else:
                log_message(f"Original file not found: {original_file_path}", log_file_path)
        except Exception as e:
            log_message(f"Error reading or deleting original file: {e}", log_file_path)
            return
    else:
        log_message(f"package.yaml not found at {package_yaml_path}", log_file_path)
        return

    # 记录skip.py日志结束
    log_message("[skip.py] XC Logs done.", log_file_path)
    sys.stdout = sys.__stdout__  # 恢复标准输出

    # 执行package.py脚本
    package_script_path = os.path.join(openjlc_dir, 'workspace', 'package.py')
    if os.path.exists(package_script_path):
        try:
            subprocess.run(['python', package_script_path], check=True)
            print(f"Package script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing package script: {e}")
    else:
        print(f"Package script {package_script_path} not found.")

if __name__ == "__main__":
    main()
