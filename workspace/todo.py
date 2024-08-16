import os
import sys
import shutil
import subprocess
import time

def main():
    # 获取OpenJLC路径
    openjlc_dir = os.environ.get("OpenJLC")
    if not openjlc_dir:
        print("Error: OpenJLC environment variable is not set.")
        sys.exit(1)

    print(f"OpenJLC path: {openjlc_dir}")

    # 定义init.py的路径
    init_script = os.path.join(openjlc_dir, 'init.py')
    if os.path.exists(init_script):
        try:
            subprocess.run(['python', init_script], check=True)
            print(f"Init script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing init script: {e}")
            sys.exit(1)
    else:
        print(f"Error: {init_script} not found.")
        sys.exit(1)

    # 延时2.1秒
    time.sleep(2.1)

    # 定义PCB下单必读.txt的路径
    output_file = os.path.join(openjlc_dir, 'output', 'PCB下单必读.txt')
    gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')

    print(f"Looking for file: {output_file}")
    if os.path.exists(output_file):
        try:
            shutil.copy2(output_file, gerber_dir)
            print(f"Copied {output_file} to {gerber_dir}")
        except Exception as e:
            print(f"Error copying file: {e}")
            sys.exit(1)
    else:
        print(f"Error: {output_file} not found.")
        sys.exit(1)

    # 等待0.5秒
    time.sleep(0.5)

    # 打开convert.py并执行
    convert_script = os.path.join(openjlc_dir, 'workspace', 'convert.py')
    if os.path.exists(convert_script):
        try:
            subprocess.run(['python', convert_script], check=True)
            print(f"Convert script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing convert script: {e}")
            sys.exit(1)
    else:
        print(f"Error: {convert_script} not found.")
        sys.exit(1)

    print("Todo script completed.")

if __name__ == "__main__":
    main()
