import os
import re
import yaml
import shutil
from datetime import datetime
import subprocess

def main():
    # 获取OpenJLC路径
    openjlc_dir = os.environ.get("OpenJLC")
    if not openjlc_dir:
        print("Error: OpenJLC environment variable is not set.")
        return

    # 定义Gerber和workflow目录
    gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')
    workflow_dir = os.path.join(openjlc_dir, 'workspace', 'workflow')
    report_file_path = os.path.join(openjlc_dir, 'workspace', 'report.yaml')
    package_yaml_path = os.path.join(openjlc_dir, 'workspace', 'package.yaml')

    # 清空workflow目录
    if os.path.exists(workflow_dir):
        shutil.rmtree(workflow_dir)
    os.makedirs(workflow_dir)
    print(f"Cleared and recreated workflow directory: {workflow_dir}")

    # 复制Gerber目录到workflow目录
    try:
        shutil.copytree(gerber_dir, workflow_dir, dirs_exist_ok=True)
        print(f"Copied {gerber_dir} to {workflow_dir}")
    except Exception as e:
        print(f"Error copying files: {e}")
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
                print(f"Matched {key} with file {file_name}")
                break

    # 保存报告到report.yaml
    try:
        with open(report_file_path, 'w', encoding='utf-8') as report_file:
            yaml.dump(report_data, report_file, default_flow_style=False, allow_unicode=True)
        print(f"Report generated at {report_file_path}")
    except Exception as e:
        print(f"Error writing report: {e}")
        return

    # 读取package.yaml文件，删除源文件
    if os.path.exists(package_yaml_path):
        try:
            with open(package_yaml_path, 'r', encoding='utf-8') as f:
                package_data = yaml.safe_load(f)
                original_file_path = os.path.join(package_data['original'], package_data['name'])

            if os.path.exists(original_file_path):
                os.remove(original_file_path)
                print(f"Deleted original file: {original_file_path}")
            else:
                print(f"Original file not found: {original_file_path}")
        except Exception as e:
            print(f"Error reading or deleting original file: {e}")
            return
    else:
        print(f"package.yaml not found at {package_yaml_path}")
        return

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
