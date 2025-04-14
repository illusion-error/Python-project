import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

# 读取文件
file_path = r"D:\HuaweiMoveData\Users\符雨晗\Desktop\价格-销量.xlsx"
try:
    df = pd.read_excel(file_path, engine='openpyxl')
except FileNotFoundError:
    print(f"错误：未找到文件 {file_path}")
except Exception as e:
    print(f"发生未知错误：{e}")
else:
    # 数据清洗
    df['价格'] = pd.to_numeric(df['价格'], errors='coerce')
    df['销量'] = pd.to_numeric(df['销量'], errors='coerce')
    df = df.dropna(subset=['价格', '销量'])

    # 按价格划分高、中、低三档
    price_quantiles = df['价格'].quantile([1 / 3, 2 / 3])
    low_threshold = price_quantiles[1 / 3]
    high_threshold = price_quantiles[2 / 3]

    def categorize_price(price):
        if price < low_threshold:
            return '低'
        elif price < high_threshold:
            return '中'
        return '高'

    df['价格区间'] = df['价格'].apply(categorize_price)

    # 设置图片清晰度
    plt.rcParams['figure.dpi'] = 300

    # 减小图形尺寸
    plt.figure(figsize=(5, 3))
    sns.boxplot(x='价格区间', y='销量', data=df, order=['低', '中', '高'])
    plt.title('不同价格区间的销量分布', fontsize=12)
    plt.xlabel('价格区间', fontsize=10)
    # 取消 x 轴标题旋转
    plt.xticks(rotation=0, fontsize=8)
    plt.ylabel('销量', fontsize=10)

    # 计算各价格区间的销量统计信息
    stats = df.groupby('价格区间')['销量'].describe()

    # 在图中添加文本说明
    for i, price_range in enumerate(['低', '中', '高']):
        median = stats.loc[price_range, '50%']
        plt.text(i, median, f"中位数: {median:.0f}", ha='center', va='center', fontsize=8, color='red')

    # 控制台输出分析描述
    print("不同价格区间销量分布分析：")
    for price_range in ['低', '中', '高']:
        print(f"价格区间: {price_range}")
        print(f"  - 平均销量: {stats.loc[price_range, 'mean']:.2f}")
        print(f"  - 中位数销量: {stats.loc[price_range, '50%']:.2f}")
        print(f"  - 最小销量: {stats.loc[price_range, 'min']:.2f}")
        print(f"  - 最大销量: {stats.loc[price_range, 'max']:.2f}")
        print(f"  - 销量标准差: {stats.loc[price_range, 'std']:.2f}")

    # 调整图形边距
    plt.subplots_adjust(top=0.9, bottom=0.15, left=0.1, right=0.95)
    # 自动调整子图参数
    plt.tight_layout()
    plt.show()
    
