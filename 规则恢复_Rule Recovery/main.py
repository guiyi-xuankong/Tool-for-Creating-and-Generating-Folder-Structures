import os
import json
import logging
import sys

def create_folder_structure(folder_structure, base_path=""):
    # 根据文件夹结构创建文件夹
    for folder_name, subfolders in folder_structure.items():
        folder_path = os.path.join(base_path, folder_name)
        create_folder(folder_path)
        if subfolders:
            create_folder_structure(subfolders, folder_path)

def create_folder(path):
    # 创建文件夹
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"创建文件夹：{path}")
    else:
        logging.info(f"文件夹已存在：{path}")

def load_folder_structure_from_config(file_path):
    # 从配置文件中加载文件夹结构
    try:
        with open(file_path, "r") as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        logging.error(f"配置文件不存在：{file_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"配置文件格式错误：{file_path}")
        return None

def get_valid_base_path():
    # 获取有效的基础路径
    base_path = input("请输入基础路径：")
    while True:
        if os.path.isdir(base_path):
            return base_path
        else:
            logging.error("路径不存在，请重新输入。")
            base_path = input("请输入基础路径：")

def confirm_base_path():
    # 确认基础路径
    choice = input("是否使用内置基础路径[选择配置文件]（D:/MyFolder/）？（输入Y或N）：")
    while choice.lower() not in ["y", "n"]:
        logging.error("输入无效，请重新输入。")
        choice = input("是否使用内置基础路径[选择配置文件]（D:/MyFolder/）？（输入Y或N）：")
    if choice.lower() == "y":
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        return get_valid_base_path()

def get_json_files_in_path(path):
    # 获取路径下的所有 JSON 文件
    json_files = []
    for file_name in os.listdir(path):
        if file_name.endswith(".json"):
            json_files.append(file_name)
    return json_files

def select_config_file(base_path):
    # 让用户选择配置文件
    json_files = get_json_files_in_path(base_path)
    print("可用的配置文件：")
    for i, file_name in enumerate(json_files):
        print(f"{i+1}. {file_name}")
    choice = input("请选择配置文件（输入对应的数字）：")
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(json_files):
        logging.error("输入无效，请重新输入。")
        choice = input("请选择配置文件（输入对应的数字）：")
    selected_file = json_files[int(choice) - 1]
    return os.path.join(base_path, selected_file)

def get_default_output_path():
    # 获取默认的文件创建路径（当前目录）
    return os.getcwd()

def select_output_path():
    # 让用户选择创建文件的路径
    choice = input("是否使用默认文件创建路径（当前目录）？（输入Y或N）：")
    while choice.lower() not in ["y", "n"]:
        logging.error("输入无效，请重新输入。")
        choice = input("是否使用默认文件创建路径（当前目录）？（输入Y或N）：")
    if choice.lower() == "y":
        return get_default_output_path()
    else:
        return get_valid_base_path()

def setup_logging():
    # 设置日志记录
    logging.basicConfig(filename="folder_creation.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    setup_logging()
    logging.info("开始执行文件夹创建程序")
    base_path = confirm_base_path()
    logging.info(f"基础路径：{base_path}")
    config_file = select_config_file(base_path)
    logging.info(f"选择的配置文件：{config_file}")
    default_output_path = get_default_output_path()
    output_path = select_output_path()
    logging.info(f"默认文件创建路径：{default_output_path}")
    logging.info(f"用户选择的文件创建路径：{output_path}")

    if os.path.isfile(config_file):
        folder_structure = load_folder_structure_from_config(config_file)
        if folder_structure:
            logging.info("开始创建文件夹结构")
            create_folder_structure(folder_structure, default_output_path)
            create_folder_structure(folder_structure, output_path)
            logging.info("文件夹结构创建完成")
    else:
        logging.error(f"配置文件不存在：{config_file}")

    logging.info("文件夹创建程序执行完成")

if __name__ == "__main__":
    main()
