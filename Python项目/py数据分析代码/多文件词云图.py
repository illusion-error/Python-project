import os
import pandas as pd

folder_path = r"D:\HuaweiMoveData\Users\符雨晗\Desktop\整理后数据\二手平台（孔夫子旧书网）"
dfs = []

for file_name in os.listdir(folder_path):
    # 过滤掉以 ~$ 开头的临时文件
    if file_name.endswith('.xlsx') and not file_name.startswith('~$'):
        file_path = os.path.join(folder_path, file_name)
        try:
            df = pd.read_excel(file_path)
            dfs.append(df)
        except Exception as e:
            print(f"读取文件 {file_name} 时出现错误: {e}")

if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)
    output_file = r"D:\HuaweiMoveData\Users\符雨晗\Desktop\整理后数据\合并后的文件.xlsx"
    merged_df.to_excel(output_file, index=False)
    print(f"合并完成，结果保存到 {output_file}")
else:
    print("未找到有效的 Excel 文件进行合并。")
