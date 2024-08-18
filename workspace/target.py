import os
import yaml
import subprocess
import sys  # 添加此行以导入 sys 模块
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

    # 记录日志开始
    log_message("[target.py] XC Logs start collecting.", log_file_path)

    # 解析target.yaml文件
    target_yaml_path = os.path.join(openjlc_dir, 'workspace', 'target.yaml')
    with open(target_yaml_path, 'r', encoding='utf-8') as f:
        target_config = yaml.safe_load(f)
    
    target_edge = target_config.get('TargetEdge')
    target_eda = target_config.get('EDA')

    # 如果EDA是LCEDA，则执行skip.py然后退出
    if target_eda == 'LCEDA':
        skip_script = os.path.join(openjlc_dir, 'workspace', 'skip.py')
        if os.path.exists(skip_script):
            subprocess.run(['python', skip_script], check=True)
        log_message("LCEDA detected, skipping further processing.", log_file_path)
        log_message("[target.py] XC Logs done.", log_file_path)
        sys.stdout = sys.__stdout__  # 恢复标准输出
        return

    # 解析config.yaml文件
    config_yaml_path = os.path.join(openjlc_dir, 'workspace', 'config.yaml')
    with open(config_yaml_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    # 根据TargetEdge和EDA设置Edge和Rule字段
    edge_mapping_ad = {
        'GKO': '2',
        'GM1': '1',
        'GM13': '3'
    }
    
    edge_mapping_kicad = {
        'Edge_Cuts': '1',
        'GM1': '2'
    }
    
    rule_mapping = {
        'Altium_Designer': 'AD',
        'KiCAD': 'KiCAD'
    }

    # 设置Edge字段
    if target_eda == 'Altium_Designer':
        edge_value = edge_mapping_ad.get(target_edge, '1')
    elif target_eda == 'KiCAD':
        edge_value = edge_mapping_kicad.get(target_edge, '1')
    else:
        edge_value = '1'

    config_data['Edge'] = edge_value
    log_message(f"Set Edge to: {edge_value}", log_file_path)

    # 设置Rule字段
    rule_value = rule_mapping.get(target_eda)
    if rule_value:
        config_data['Rule'] = rule_value
        log_message(f"Set Rule to: {rule_value}", log_file_path)

    # 更新config.yaml文件
    with open(config_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
    log_message(f"Updated config.yaml with Edge: {config_data['Edge']} and Rule: {config_data['Rule']}", log_file_path)

    # 执行convert.py脚本
    convert_script = os.path.join(openjlc_dir, 'workspace', 'convert.py')
    if os.path.exists(convert_script):
        try:
            subprocess.run(['python', convert_script], check=True)
            log_message(f"Convert script executed successfully.", log_file_path)
        except subprocess.CalledProcessError as e:
            log_message(f"Error executing convert script: {e}", log_file_path)
    else:
        log_message(f"Convert script {convert_script} not found.", log_file_path)

    # 记录日志结束
    log_message("[target.py] XC Logs done.", log_file_path)
    sys.stdout = sys.__stdout__  # 恢复标准输出

if __name__ == "__main__":
    main()
