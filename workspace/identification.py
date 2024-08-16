import os
import re
import yaml
import subprocess

def main():
    # 获取OpenJLC路径
    openjlc_dir = os.environ.get("OpenJLC")
    if not openjlc_dir:
        print("Error: OpenJLC environment variable is not set.")
        return

    # 解析identification.yaml文件
    identification_yaml_path = os.path.join(openjlc_dir, 'rule', 'identification.yaml')
    with open(identification_yaml_path, 'r', encoding='utf-8') as f:
        identification_config = yaml.safe_load(f)
    
    target_eda = identification_config.get('TargetEDA', 'Auto')
    edge_config = identification_config.get('Edge', 'Auto')
    identification_file_pattern = identification_config.get('IdentificationFile', r'(?i)(\.gm1|\.gko|\.gm13|Edge_Cuts|-Edge_Cuts)')

    # 定义目标文件路径
    target_yaml_path = os.path.join(openjlc_dir, 'workspace', 'target.yaml')

    # 处理Edge配置
    if edge_config != 'Auto':
        if edge_config in ['GKO', 'Edge_Cuts', 'GM1', 'GM13']:
            # 删除旧的target.yaml文件
            if os.path.exists(target_yaml_path):
                os.remove(target_yaml_path)

            # 创建新的target.yaml文件并写入Edge信息
            with open(target_yaml_path, 'w', encoding='utf-8') as f:
                f.write(f"TargetEdge: {edge_config}\n")
                f.write("#TargetEdge: Edge_Cuts\n")
                f.write("#TargetEdge: GM1\n")
                f.write("#TargetEdge: GM13\n")
        else:
            print("Invalid Edge configuration specified.")
            return
    else:
        # Auto模式下，查找文件
        gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')
        found_file = None

        for root, dirs, files in os.walk(gerber_dir):
            for file in files:
                if re.search(identification_file_pattern, file, re.IGNORECASE):
                    found_file = os.path.join(root, file)
                    break
            if found_file:
                break

        if found_file:
            print(f"Found edge file: {found_file}")

            # 确定匹配的Edge类型
            if re.search(r'\.gm1', found_file, re.IGNORECASE):
                target_edge = 'GM1'
            elif re.search(r'\.gko', found_file, re.IGNORECASE):
                target_edge = 'GKO'
            elif re.search(r'Edge_Cuts', found_file, re.IGNORECASE):
                target_edge = 'Edge_Cuts'
            elif re.search(r'\.gm13', found_file, re.IGNORECASE):
                target_edge = 'GM13'
            else:
                target_edge = 'Unknown'

            # 写入TargetEdge到target.yaml
            with open(target_yaml_path, 'w', encoding='utf-8') as f:
                f.write(f"TargetEdge: {target_edge}\n")
                f.write("#TargetEdge: Edge_Cuts\n")
                f.write("#TargetEdge: GM1\n")
                f.write("#TargetEdge: GM13\n")
            print(f"Identified TargetEdge: {target_edge}")

            # 寻找EDA信息
            with open(found_file, 'r', encoding='utf-8') as f:
                first_21_lines = [next(f) for _ in range(21)]
                first_21_text = ''.join(first_21_lines)

            if 'Altium' in first_21_text:
                eda_tool = 'Altium_Designer'
            elif 'KiCad' in first_21_text:
                eda_tool = 'KiCAD'
            elif 'EasyEDA' in first_21_text:
                eda_tool = 'LCEDA'
            else:
                eda_tool = None

            if eda_tool:
                # 写入EDA信息到target.yaml
                with open(target_yaml_path, 'a', encoding='utf-8') as f:
                    f.write(f"EDA: {eda_tool}\n")
                    f.write("#EDA: Altium_Designer\n")
                    f.write("#EDA: KiCAD\n")
                    f.write("#EDA: LCEDA\n")
                print(f"Identified EDA tool: {eda_tool}")
            else:
                print("Could not identify EDA tool.")
        else:
            print("No matching edge file found.")
            return

    # 如果identification.yaml中的TargetEDA已经被指定
    if target_eda != 'Auto':
        eda_mapping = {
            'Altium_Designer': 'Altium_Designer',
            'KiCAD': 'KiCAD',
            'LCEDA': 'LCEDA'
        }

        if eda_mapping.get(target_eda):
            # 写入目标EDA到target.yaml
            with open(target_yaml_path, 'a', encoding='utf-8') as f:
                f.write(f"EDA: {eda_mapping[target_eda]}\n")
                f.write("#EDA: Altium_Designer\n")
                f.write("#EDA: KiCAD\n")
                f.write("#EDA: LCEDA\n")
            print(f"Specified EDA tool: {target_eda}")

    # 执行target.py脚本
    target_script_path = os.path.join(openjlc_dir, 'workspace', 'target.py')
    if os.path.exists(target_script_path):
        try:
            subprocess.run(['python', target_script_path], check=True)
            print(f"Target script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing target script: {e}")
        return
    else:
        print(f"Target script {target_script_path} not found.")

if __name__ == "__main__":
    main()
