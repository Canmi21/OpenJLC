import os
import shutil

def clear_directory(directory):
    try:
        # 检查文件夹是否存在
        if os.path.exists(directory):
            # 遍历文件夹中的所有内容
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                # 如果是文件或符号链接，删除它
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # 如果是目录，递归删除它
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            print(f"Cleared contents of directory: {directory}")
        else:
            print(f"Directory does not exist: {directory}")
    except Exception as e:
        print(f"Error clearing directory {directory}: {e}")

def main():
    # 获取OpenJLC路径
    openjlc_dir = os.environ.get("OpenJLC")
    if not openjlc_dir:
        print("Error: OpenJLC environment variable is not set.")
        return

    # 定义需要清理的目录
    gerber_dir = os.path.join(openjlc_dir, 'workspace', 'Gerber')
    workflow_dir = os.path.join(openjlc_dir, 'workspace', 'workflow')

    # 清理Gerber和workflow目录
    clear_directory(gerber_dir)
    clear_directory(workflow_dir)

if __name__ == "__main__":
    main()
