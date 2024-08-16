import yaml
import os
import re
import shutil
from datetime import datetime
import subprocess  # 用于执行package.py

# 获取OpenJLC路径
openjlc_dir = os.environ.get("OpenJLC")
if not openjlc_dir:
    print("Error: OpenJLC environment variable is not set.")
    exit(1)

# 设置工作目录和目标目录
WorkDir = os.path.join(openjlc_dir, 'workspace', 'Gerber')
DestDir = os.path.join(openjlc_dir, 'workspace', 'workflow')

# 固定读取config.yaml的路径
config_file = os.path.join(openjlc_dir, "workspace", "config.yaml")
print(f"Config file path: {config_file}")

# 加载配置文件
try:
    with open(config_file, "r", encoding="utf-8") as fconfig:
        Config = yaml.load(fconfig, Loader=yaml.FullLoader)
        print("Config file loaded successfully.")
except FileNotFoundError as e:
    print(f"Failed to load config file: {e}")
    exit(1)
except Exception as e:
    print(f"Error while loading config file: {e}")
    exit(1)

# 从固定路径读取Header
header_file = os.path.join(openjlc_dir, "config", "Header.yaml")
print(f"Header file path: {header_file}")

# 加载Header文件
try:
    with open(header_file, "r", encoding="utf-8") as fheader:
        HeaderConfig = yaml.load(fheader, Loader=yaml.FullLoader)
        print("Header file loaded successfully.")
except FileNotFoundError as e:
    print(f"Failed to load header file: {e}")
    exit(1)
except Exception as e:
    print(f"Error while loading header file: {e}")
    exit(1)

# 从配置文件中获取规则类型和边缘类型
rule_type = Config.get("Rule")
edge_type = Config.get("Edge")

# 调试信息
print(f"Rule type: {rule_type}")
print(f"Edge type: {edge_type}")

if not rule_type or not edge_type:
    print("Error: Rule type or Edge type is not defined in config.yaml")
    exit(1)

# 根据Rule类型加载对应的规则文件
if rule_type == "AD":
    rule_file = os.path.join(openjlc_dir, "rule", "rule_altium_designer.yaml")
elif rule_type == "KiCAD":
    rule_file = os.path.join(openjlc_dir, "rule", "rule_kicad.yaml")
else:
    print(f"Error: Unknown Rule type '{rule_type}' in config.yaml")
    exit(1)

print(f"Rule file path: {rule_file}")

# 加载规则文件
try:
    with open(rule_file, "r", encoding="utf-8") as frule:
        Rule = yaml.load(frule, Loader=yaml.FullLoader)
        print("Rule file loaded successfully.")
except FileNotFoundError as e:
    print(f"Failed to load rule file: {e}")
    exit(1)
except Exception as e:
    print(f"Error while loading rule file: {e}")
    exit(1)

# 根据Edge类型选择正确的Outline规则
outline_key = f"Outline{edge_type}"
if outline_key in Rule:
    Rule["Outline"] = Rule[outline_key]
    print(f"Using Outline rule: {outline_key}")
else:
    print(f"Error: Outline rule for Edge '{edge_type}' not found in {rule_file}")
    exit(1)

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
        print(f"Config key '{key}' found.")

# 清空目标目录
if os.path.exists(DestDir):
    try:
        shutil.rmtree(DestDir)
        print(f"Cleared destination directory: {DestDir}")
    except Exception as e:
        print(f"Error clearing destination directory: {e}")
        exit(1)

# 重新创建目标目录
os.makedirs(DestDir)
print(f"Created destination directory: {DestDir}")

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

    print(f"Searching for files matching rule '{key}'...")

    for fileName in os.listdir(WorkDir):
        if rePattern.search(fileName):
            matchFile.append(fileName)

    if len(matchFile) < 1:
        print(f"{key} match failed, skipping this file.")
        report[key] = "No"
        continue
    elif len(matchFile) > 1:
        raise Exception(f"{key} multiple matches found: {', '.join(matchFile)}")
    else:
        print(f"{key} -> {matchFile[0]}")
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
            print(f"Processed file '{matchFile}' and saved to '{dest_file_path}'")
        except Exception as e:
            print(f"Error processing file '{matchFile}': {e}")
            exit(1)
    else:
        print(f"File matching rule '{key}' not found.")
        report[key] = "No"

# 将报告写入 report.yaml 文件
report_file_path = os.path.join(openjlc_dir, "workspace", "report.yaml")
try:
    with open(report_file_path, "w", encoding="utf-8") as report_file:
        yaml.dump(report, report_file, default_flow_style=False, allow_unicode=True)
    print(f"Report generated successfully at {report_file_path}")
except Exception as e:
    print(f"Error generating report: {e}")

# 执行package.py
package_script = os.path.join(openjlc_dir, 'workspace', 'package.py')
if os.path.exists(package_script):
    try:
        subprocess.run(['python', package_script], check=True)
        print(f"Package script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing package script: {e}")
        exit(1)
else:
    print(f"Error: {package_script} not found.")
    exit(1)
