import os
import yaml
import subprocess

def main():
    # 获取OpenJLC路径
    openjlc_dir = os.environ.get("OpenJLC")
    if not openjlc_dir:
        print("Error: OpenJLC environment variable is not set.")
        return

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
        print("LCEDA detected, skipping further processing.")
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
    print(f"Set Edge to: {edge_value}")

    # 设置Rule字段
    rule_value = rule_mapping.get(target_eda)
    if rule_value:
        config_data['Rule'] = rule_value
        print(f"Set Rule to: {rule_value}")

    # 更新config.yaml文件
    with open(config_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
    print(f"Updated config.yaml with Edge: {config_data['Edge']} and Rule: {config_data['Rule']}")

    # 执行convert.py脚本
    convert_script = os.path.join(openjlc_dir, 'workspace', 'convert.py')
    if os.path.exists(convert_script):
        try:
            subprocess.run(['python', convert_script], check=True)
            print(f"Convert script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing convert script: {e}")
    else:
        print(f"Convert script {convert_script} not found.")

if __name__ == "__main__":
    main()
