import os
import shutil

# 定义要操作的文件夹路径
folder_path = "/path/to/your/folder"


# 获取文件夹列表
folders = os.listdir(folder_path)

# 遍历每个文件夹
for folder in folders:
    folder_dir = os.path.join(folder_path, folder)

    # 如果是文件夹
    if os.path.isdir(folder_dir):

        # 删除evaluator和data文件夹
        evaluator_dir = os.path.join(folder_dir, "evaluator")
        data_dir = os.path.join(folder_dir, "data")
        figures_dir = os.path.join(folder_dir, "figures")
        if os.path.exists(evaluator_dir):
            shutil.rmtree(evaluator_dir)
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)
        if os.path.exists(figures_dir):
            shutil.rmtree(figures_dir)

        # 处理apprfunc文件夹
        apprfunc_dir = os.path.join(folder_dir, "apprfunc")
        if os.path.exists(apprfunc_dir) and os.path.isdir(apprfunc_dir):
            files = os.listdir(apprfunc_dir)
            for file in files:
                file_path = os.path.join(apprfunc_dir, file)

                # 删除不以"_opt.pkl"结尾的.pkl文件
                if file.endswith(".pkl") and not file.endswith("_opt.pkl") and not file.endswith("1500000.pkl"):
                    os.remove(file_path)
