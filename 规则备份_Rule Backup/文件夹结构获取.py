import platform
import os
import subprocess
import sys
import json

def run_as_admin():
    system = platform.system()

    if system == 'Windows':
        import ctypes

        def is_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        if not is_admin():
            print("当前没有管理员权限，是否尝试使用管理员权限重新运行？（Y或N）")
            choice = input("> ")
            if choice.lower() == "y":
                print("重新运行中...")
                args = ['python'] + sys.argv
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(args), None, 1)
                sys.exit()
            else:
                print("程序将以普通权限继续运行...")

    elif system == 'Linux' or system == 'Darwin':  # Mac OS
        if os.getuid() != 0:
            print("请使用管理员权限运行此脚本！")
            args = ['sudo', 'python3'] + sys.argv
            subprocess.run(args)
            sys.exit()


# 调用函数以检查并以管理员权限运行脚本
run_as_admin()

def generate_folder_structure(root_path):
    """
    递归生成文件夹结构规则

    Args:
        root_path (str): 根文件夹路径

    Returns:
        dict: 文件夹结构规则
    """
    folder_structure = {}
    generate_folder_structure_recursive(root_path, folder_structure)
    return folder_structure

def generate_folder_structure_recursive(path, folder_structure):
    """
    递归生成文件夹结构规则

    Args:
        path (str): 当前文件夹路径
        folder_structure (dict): 文件夹结构规则
    """
    folder_name = os.path.basename(path)
    subfolders = []

    try:
        subfolders = [f.name for f in os.scandir(path) if f.is_dir() and os.access(f.path, os.R_OK)]
    except PermissionError as e:
        print(f"访问权限被拒绝，无法获取子文件夹列表。路径: {path}")
        print(f"错误信息: {str(e)}")

    if subfolders:
        folder_structure[folder_name] = {}

        for subfolder in subfolders:
            subfolder_path = os.path.join(path, subfolder)
            generate_folder_structure_recursive(subfolder_path, folder_structure[folder_name])

def select_folders_from_path(path):
    """
    从指定路径获取文件夹列表

    Args:
        path (str): 指定路径

    Returns:
        list: 文件夹列表
    """
    subfolders = []

    try:
        subfolders = [f.name for f in os.scandir(path) if f.is_dir() and os.access(f.path, os.R_OK)]
    except PermissionError as e:
        print(f"访问权限被拒绝，无法获取文件夹列表。路径: {path}")
        print(f"错误信息: {str(e)}")

    return subfolders

# 根据操作系统选择输入方式
system = platform.system()
if system == 'Windows':
    drive_letter = input("请输入盘符：")
    root_path = f"{drive_letter}:\\"
elif system == 'Linux' or system == 'Darwin':  # Mac OS
    root_path = input("请输入根文件夹路径：")

# 检查输入路径是否存在
if not os.path.exists(root_path):
    print("指定的路径不存在！")
    sys.exit()

# 获取根文件夹下的所有文件夹
folders = select_folders_from_path(root_path)

# 提示用户选择文件夹
print("可用的文件夹列表：")
for i, folder in enumerate(folders):
    print(f"{i+1}. {folder}")

# 用户选择文件夹
selection = input("请选择文件夹（多个文件夹用逗号分隔，输入0表示全选）：")

if selection == "0":
    selected_folders = folders
else:
    selected_indexes = selection.split(".")
    selected_folders = []

    # 验证用户输入的索引是否有效
    for index in selected_indexes:
        if index.isdigit() and int(index) > 0 and int(index) <= len(folders):
            selected_folders.append(folders[int(index) - 1])

# 打印所选的文件夹
print("所选文件夹：", selected_folders)

# 生成文件夹结构规则并保存到文件
for folder in selected_folders:
    # 生成指定文件夹的文件夹结构规则
    folder_structure = generate_folder_structure(os.path.join(root_path, folder))

    # 设置文件的保存路径
    output_path = f"{folder}_structure.json"

    # 将文件夹结构规则写入到文件中
    with open(output_path, "w") as file:
        json.dump(folder_structure, file, indent=4)

    # 打印保存文件的路径
    print(f"文件夹 {folder} 的结构规则已生成并保存到 {os.path.abspath(output_path)} 文件中。")
