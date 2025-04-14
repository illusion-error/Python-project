# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from tqdm import tqdm

# ==============================
# 1. 基础设置
# ==============================
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==============================
# 2. 数据读取
# ==============================
def load_data(file_path):
    """加载Excel数据并处理基础格式"""
    try:
        df = pd.read_excel(file_path)
        print("数据加载成功，样本量：", len(df))
        return df
    except Exception as e:
        print(f"数据加载失败：{str(e)}")
        exit()

file_path = r"D:\HuaweiMoveData\Users\符雨晗\Desktop\订单.xlsx"
raw_df = load_data(file_path)

# ==============================
# 3. 日期转换处理
# ==============================
def convert_excel_date(excel_serial):
    """处理Excel序列日期（如42826）"""
    try:
        base_date = datetime(1899, 12, 30)
        delta = timedelta(days=int(float(excel_serial)))
        return base_date + delta
    except:
        return pd.NaT

def convert_to_quarter(date_str):
    """万能日期转换函数"""
    original = str(date_str).strip()
    
    # 场景1：Excel序列数
    if original.replace(".", "", 1).isdigit():
        dt = convert_excel_date(original)
        if pd.isnull(dt):
            return np.nan
        return f"{dt.year}-Q{(dt.month-1)//3 + 1}"
    
    # 场景2：中文年月（2016年4月）
    if "年" in original and "月" in original:
        parts = original.replace("年", "-").replace("月", "").split("-")
        if len(parts) == 2:
            year, month = parts
            return f"{year}-Q{(int(month)-1)//3 + 1}"
    
    # 场景3：季度简写（2021Q3）
    if "Q" in original.upper():
        parts = original.upper().split("Q")
        if len(parts) == 2:
            return f"{parts[0]}-Q{parts[1]}"
    
    # 场景4：标准季度格式（2021-Q3）
    if "-Q" in original:
        return original
    
    return np.nan

# 应用转换函数
tqdm.pandas(desc="日期转换进度")
raw_df['季度标识'] = raw_df['季度（时间）'].progress_apply(convert_to_quarter)

# ==============================
# 4. 生成标准时间序列
# ==============================
def create_quarter_date(q_str):
    """将季度标识转换为日期对象"""
    try:
        year, q = q_str.split('-Q')
        month = 3 * int(q) - 2  # Q1→1月，Q2→4月，Q3→7月，Q4→10月
        return datetime(int(year), month, 1)
    except:
        return pd.NaT

# 生成标准日期列
raw_df['季度时间'] = raw_df['季度标识'].apply(create_quarter_date)
valid_df = raw_df.dropna(subset=['季度时间']).sort_values('季度时间')

# ==============================
# 5. 数据聚合
# ==============================
# 按季度聚合数据
agg_config = {
    '价格': 'mean',
    '销量': 'sum'
}

quarterly = valid_df.groupby(
    pd.Grouper(key='季度时间', freq='QE')
).agg(agg_config).reset_index()

# 填充缺失季度（前向填充）
full_range = pd.date_range(
    start=quarterly['季度时间'].min(),
    end=quarterly['季度时间'].max(),
    freq='QE'
)
quarterly = quarterly.set_index('季度时间').reindex(full_range).ffill().reset_index()
quarterly.rename(columns={'index': '季度时间'}, inplace=True)

# ==============================
# 6. 价格弹性计算
# ==============================
def calculate_elasticity(df):
    """对数差分法计算价格弹性"""
    df = df.copy()
    df['ln_price'] = np.log(df['价格'])
    df['ln_quantity'] = np.log(df['销量'])
    df['价格弹性'] = df['ln_quantity'].diff() / df['ln_price'].diff()
    
    # 处理极端值
    df['价格弹性'] = np.where(
        (df['价格弹性'].abs() > 5) | (df['价格弹性'].isna()),
        np.nan,
        df['价格弹性']
    )
    return df

quarterly = calculate_elasticity(quarterly)

# 保持其他部分不变，仅修改可视化部分：

# ==============================
# 7. 可视化设置
# ==============================
plt.figure(figsize=(14, 8))
ax = plt.subplot()

# 7.1 绘制弹性曲线（保持不变）
ax.plot(quarterly['季度时间'], quarterly['价格弹性'],
        marker='o', markersize=8, linestyle='-',
        color='#1f77b4', linewidth=2,
        markerfacecolor='white', markeredgewidth=1.5)

# 7.2 政策标注设置（保持不变）
# [保持原有政策标注代码]

# 7.3 坐标轴格式化（关键修复）
def quarter_formatter(x, pos=None):
    """将matplotlib的数值日期转换为季度格式"""
    try:
        date = mdates.num2date(x)
        year = date.year
        quarter = (date.month - 1) // 3 + 1
        return f"{year}-Q{quarter}"
    except:
        return ""

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(plt.FuncFormatter(quarter_formatter))

# 7.4 图表装饰
plt.title('海南黄花梨苗木价格弹性季度分析（2016-2024）', fontsize=16, pad=20)
plt.xlabel('季度', fontsize=12, labelpad=10)
plt.ylabel('价格弹性系数', fontsize=12, labelpad=10)
plt.grid(alpha=0.3, linestyle='--')
plt.xticks(rotation=45, ha='right', fontsize=10)

# 8. 输出结果（保持不变）
# [保持原有输出代码]
# ==============================
# 8. 输出结果
# ==============================
# 8.1 保存图表
output_img = r'D:\HuaweiMoveData\Users\符雨晗\Desktop\价格弹性分析_最终版.png'
plt.tight_layout()
plt.savefig(output_img, dpi=300, bbox_inches='tight')
print(f"\n分析图表已保存至：{output_img}")

# 8.2 输出数据表格
output_data = quarterly[['季度时间', '价格', '销量', '价格弹性']].copy()
output_data['季度'] = output_data['季度时间'].dt.strftime('%Y-Q%q')
output_data['价格'] = output_data['价格'].round(2)
output_data['销量'] = output_data['销量'].astype(int)

print("\n季度分析数据：")
print(output_data[['季度', '价格', '销量', '价格弹性']].to_markdown(index=False, floatfmt=".2f"))

# 8.3 显示图表
plt.show()
