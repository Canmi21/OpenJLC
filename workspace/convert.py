import yaml
import os
import re
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

    # 记录convert.py日志开始
    log_message("[convert.py] XC Logs start collecting.", log_file_path)

    # 设置工作目录和目标目录
    WorkDir = os.path.join(openjlc_dir, 'workspace', 'Gerber')
    DestDir = os.path.join(openjlc_dir, 'workspace', 'workflow')

    # 固定读取config.yaml的路径
    config_file = os.path.join(openjlc_dir, "workspace", "config.yaml")
    log_message(f"Config file path: {config_file}", log_file_path)

    # 加载配置文件
    try:
        with open(config_file, "r", encoding="utf-8") as fconfig:
            Config = yaml.load(fconfig, Loader=yaml.FullLoader)
            log_message("Config file loaded successfully.", log_file_path)
    except FileNotFoundError as e:
        log_message(f"Failed to load config file: {e}", log_file_path)
        sys.exit(1)
    except Exception as e:
        log_message(f"Error while loading config file: {e}", log_file_path)
        sys.exit(1)

    # 从固定路径读取Header
    header_file = os.path.join(openjlc_dir, "config", "Header.yaml")
    log_message(f"Header file path: {header_file}", log_file_path)

    # 加载Header文件
    try:
        with open(header_file, "r", encoding="utf-8") as fheader:
            HeaderConfig = yaml.load(fheader, Loader=yaml.FullLoader)
            log_message("Header file loaded successfully.", log_file_path)
    except FileNotFoundError as e:
        log_message(f"Failed to load header file: {e}", log_file_path)
        sys.exit(1)
    except Exception as e:
        log_message(f"Error while loading header file: {e}", log_file_path)
        sys.exit(1)

    # 从配置文件中获取规则类型和边缘类型
    rule_type = Config.get("Rule")
    edge_type = Config.get("Edge")

    # 调试信息
    log_message(f"Rule type: {rule_type}", log_file_path)
    log_message(f"Edge type: {edge_type}", log_file_path)

    if not rule_type or not edge_type:
        log_message("Error: Rule type or Edge type is not defined in config.yaml", log_file_path)
        sys.exit(1)

    # 根据Rule类型加载对应的规则文件
    if rule_type == "AD":
        rule_file = os.path.join(openjlc_dir, "rule", "rule_altium_designer.yaml")
    elif rule_type == "KiCAD":
        rule_file = os.path.join(openjlc_dir, "rule", "rule_kicad.yaml")
    else:
        log_message(f"Error: Unknown Rule type '{rule_type}' in config.yaml", log_file_path)
        sys.exit(1)

    log_message(f"Rule file path: {rule_file}", log_file_path)

    # 加载规则文件
    try:
        with open(rule_file, "r", encoding="utf-8") as frule:
            Rule = yaml.load(frule, Loader=yaml.FullLoader)
            log_message("Rule file loaded successfully.", log_file_path)
    except FileNotFoundError as e:
        log_message(f"Failed to load rule file: {e}", log_file_path)
        sys.exit(1)
    except Exception as e:
        log_message(f"Error while loading rule file: {e}", log_file_path)
        sys.exit(1)

    # 根据Edge类型选择正确的Outline规则
    outline_key = f"Outline{edge_type}"
    if outline_key in Rule:
        Rule["Outline"] = Rule[outline_key]
        log_message(f"Using Outline rule: {outline_key}", log_file_path)
    else:
        log_message(f"Error: Outline rule for Edge '{edge_type}' not found in {rule_file}", log_file_path)
        sys.exit(1)

    # 移除其他可能的Outline规则，只保留选中的
    for key in list(Rule.keys()):
        if key.startswith("Outline") and key != "Outline":
            del Rule[key]

    # 验证必要的配置项
    required_keys = ["FileName"]
    for key in required_keys:
        if key not in Config:
            raise KeyError(f"Missing required config key: {key}")
        else:
            log_message(f"Config key '{key}' found.", log_file_path)

    # 清空目标目录
    if os.path.exists(DestDir):
        try:
            shutil.rmtree(DestDir)
            log_message(f"Cleared destination directory: {DestDir}", log_file_path)
        except Exception as e:
            log_message(f"Error clearing destination directory: {e}", log_file_path)
            sys.exit(1)

    # 重新创建目标目录
    os.makedirs(DestDir)
    log_message(f"Created destination directory: {DestDir}", log_file_path)

    # 创建报告字典
    report = {
        "Source": rule_type,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Edge": "Yes" if Rule.get("Outline") else "No"
    }

    # 检验文件是否齐全/重复匹配
    for key, value in Rule.items():
        matchFile = []
        rePattern = re.compile(pattern=value, flags=re.IGNORECASE)  # 添加忽略大小写

        log_message(f"Searching for files matching rule '{key}'...", log_file_path)

        for fileName in os.listdir(WorkDir):
            if rePattern.search(fileName):
                matchFile.append(fileName)

        if len(matchFile) < 1:
            log_message(f"{key} match failed, skipping this file.", log_file_path)
            report[key] = "No"
            continue
        elif len(matchFile) > 1:
            raise Exception(f"{key} multiple matches found: {', '.join(matchFile)}")
        else:
            log_message(f"{key} -> {matchFile[0]}", log_file_path)
            report[key] = "Yes"

    # 改名和加头操作
    for key, value in Rule.items():
        rePattern = re.compile(pattern=value, flags=re.IGNORECASE)
        matchFile = ""

        for fileName in os.listdir(WorkDir):
            if rePattern.search(fileName):
                matchFile = fileName
                break

        if matchFile:
            dest_file_path = os.path.join(DestDir, Config["FileName"][key])
            try:
                with open(os.path.join(WorkDir, matchFile), "r") as file:
                    fileData = file.read()
                with open(dest_file_path, "w", encoding="utf-8") as file:
                    file.write(HeaderConfig["Header"])  # 使用从Header.yaml加载的Header
                    file.write(fileData)
                log_message(f"Processed file '{matchFile}' and saved to '{dest_file_path}'", log_file_path)
            except Exception as e:
                log_message(f"Error processing file '{matchFile}': {e}", log_file_path)
                sys.exit(1)
        else:
            log_message(f"File matching rule '{key}' not found.", log_file_path)
            report[key] = "No"

    # 将报告写入 report.yaml 文件
    report_file_path = os.path.join(openjlc_dir, "workspace", "report.yaml")
    try:
        with open(report_file_path, "w", encoding="utf-8") as report_file:
            yaml.dump(report, report_file, default_flow_style=False, allow_unicode=True)
        log_message(f"Report generated successfully at {report_file_path}", log_file_path)
    except Exception as e:
        log_message(f"Error generating report: {e}", log_file_path)

    # 记录convert.py日志结束
    log_message("[convert.py] XC Logs done.", log_file_path)
    sys.stdout = sys.__stdout__  # 恢复标准输出

    # 执行package.py
    package_script = os.path.join(openjlc_dir, 'workspace', 'package.py')
    if os.path.exists(package_script):
        try:
            subprocess.run(['python', package_script], check=True)
            print(f"Package script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing package script: {e}")
            sys.exit(1)
    else:
        print(f"Error: {package_script} not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
