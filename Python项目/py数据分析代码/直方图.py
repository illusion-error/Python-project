import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据读取与清洗
file_path = r"D:\HuaweiMoveData\Users\符雨晗\Desktop\价格.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')
df['价格'] = pd.to_numeric(df['价格'], errors='coerce').dropna()

# 异常值过滤（保留99%数据）
price = df['价格']
Q99 = price.quantile(0.99)
filtered_price = price[price <= Q99]

# 智能分箱策略
def auto_bins(data):
    """自动生成对数分箱"""
    min_val = data.min()
    max_val = data.max()
    bins = np.logspace(np.log10(min_val), 
                      np.log10(max_val), 
                      30)
    return np.unique(bins.astype(int))

# 可视化设置
plt.figure(figsize=(14, 7))
ax = plt.gca()

# 绘制直方图（对数分箱+双坐标）
n, bins, patches = ax.hist(
    filtered_price,
    bins=auto_bins(filtered_price),
    color='#2ecc71',
    edgecolor='#27ae60',
    alpha=0.8,
    density=False
)

# 添加辅助元素
median = filtered_price.median()
mean = filtered_price.mean()
ax.axvline(median, color='#e74c3c', linestyle='--', linewidth=1.5, label=f'中位数 ({median:,.0f}元)')
ax.axvline(mean, color='#f39c12', linestyle=':', linewidth=1.5, label=f'平均值 ({mean:,.0f}元)')

# 格式化坐标轴
def yuan_formatter(x, pos):
    if x >= 1e4:
        return f'{x/1e4:.0f}万'
    return f'{x:.0f}'
ax.xaxis.set_major_formatter(FuncFormatter(yuan_formatter))

# 添加数据标签
for i in range(len(n)):
    if n[i] > 5:  # 只显示频次大于5的标签
        ax.text((bins[i] + bins[i+1])/2, n[i], 
               f'{int(n[i])}',
               ha='center', 
               va='bottom',
               fontsize=8)

# 添加图例和标题
plt.title(f'黄花梨价格分布（过滤前1%极端值，保留{n.sum():,}条数据）', fontsize=14)
plt.xlabel('价格（对数刻度）', fontsize=12)
plt.ylabel('成交数量', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.4)
plt.xscale('log')  # X轴对数刻度

# 添加统计注释
stats_text = f'''数据特征（过滤后）：
- 价格区间：{filtered_price.min():,.0f}元 ~ {Q99:,.0f}元
- 中位数：{median:,.0f}元
- 平均值：{mean:,.0f}元
- 标准差：{filtered_price.std():,.0f}元'''
plt.annotate(stats_text, 
            xy=(0.98, 0.7), 
            xycoords='axes fraction',
            ha='right',
            va='top',
            bbox=dict(boxstyle='round', alpha=0.2, facecolor='grey'))

plt.tight_layout()
plt.show()
