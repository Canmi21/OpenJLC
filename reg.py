import sys
import os
import shutil
import subprocess

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

if __name__ == "__main__":
    main()
