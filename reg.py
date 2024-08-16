import sys
import os
import shutil
import subprocess
import yaml

def main():
    # 获取OpenJLC路径
    openjlc_dir = os.environ.get("OpenJLC")
    if not openjlc_dir:
        print("Error: OpenJLC environment variable is not set.")
        sys.exit(1)

    print(f"OpenJLC path: {openjlc_dir}")

    # 检查传入的.zip文件路径
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.zip'):
        print("Usage: reg.py <zip_file_path>")
        sys.exit(1)

    zip_file_path = sys.argv[1]
    print(f"ZIP file path: {zip_file_path}")

    # 生成package.yaml报告，尽可能提前执行
    package_report_path = os.path.join(openjlc_dir, 'workspace', 'package.yaml')

    # 删除旧的package.yaml文件（如果存在）
    if os.path.exists(package_report_path):
        try:
            os.remove(package_report_path)
            print(f"Deleted old package report: {package_report_path}")
        except Exception as e:
            print(f"Error deleting old package report: {e}")
            sys.exit(1)

    # 定义报告内容
    package_report_content = {
        'original': os.path.dirname(zip_file_path).replace("\\", "/") + "/",
        'name': os.path.basename(zip_file_path)  # 使用.zip文件的原始名称
    }

    try:
        with open(package_report_path, 'w', encoding='utf-8') as report_file:
            yaml.dump(package_report_content, report_file, default_flow_style=False, allow_unicode=True)
        print(f"Package report generated at {package_report_path}")
    except Exception as e:
        print(f"Error generating package report: {e}")
        sys.exit(1)

    # 定义Gerber目录
    gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')
    
    # 确保目标文件夹存在
    if not os.path.exists(gerber_dir):
        os.makedirs(gerber_dir)
    print(f"Gerber directory: {gerber_dir}")

    # 清空Gerber目录中的所有文件
    try:
        for filename in os.listdir(gerber_dir):
            file_path = os.path.join(gerber_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 删除文件或符号链接
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 删除目录
        print(f"Cleared Gerber directory: {gerber_dir}")
    except Exception as e:
        print(f"Error clearing Gerber directory: {e}")
        sys.exit(1)

    # 复制选中的.zip文件到Gerber目录
    destination = os.path.join(gerber_dir, os.path.basename(zip_file_path))
    try:
        shutil.copy2(zip_file_path, destination)
        print(f"Copied {zip_file_path} to {destination}")
    except Exception as e:
        print(f"Error copying file: {e}")
        sys.exit(1)

    # 执行unzip.py脚本
    unzip_script = os.path.join(openjlc_dir, 'workspace', 'unzip.py')
    if os.path.exists(unzip_script):
        try:
            subprocess.run(['python', unzip_script], check=True)
            print(f"Unzip script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing unzip script: {e}")
            sys.exit(1)
    else:
        print(f"Error: {unzip_script} not found.")
        sys.exit(1)

    # 执行todo.py脚本
    todo_script = os.path.join(openjlc_dir, 'workspace', 'todo.py')
    if os.path.exists(todo_script):
        try:
            subprocess.run(['python', todo_script], check=True)
            print(f"Todo script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing todo script: {e}")
            sys.exit(1)
    else:
        print(f"Error: {todo_script} not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
