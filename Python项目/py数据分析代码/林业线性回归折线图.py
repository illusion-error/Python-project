import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

# 给定的数据
years = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]).reshape(-1, 1)
output_values = np.array([4189.98, 4358.45, 4635.9, 4980.55, 5432.61, 5775.71, 5961.58, 6507.70, 6820.83, 7006.08])

# 创建线性回归模型
model = LinearRegression()

# 训练模型
model.fit(years, output_values)

# 预测 2035 年的林业总产值
target_year = np.array([2035]).reshape(-1, 1)
predicted_output = model.predict(target_year)

print(f"预测 2035 年的林业总产值为: {predicted_output[0]:.2f} 亿元")

# 生成用于绘制线性回归直线的数据
x_line = np.linspace(2014, 2035, 100).reshape(-1, 1)
y_line = model.predict(x_line)

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 绘制折线图
plt.figure(figsize=(10, 6))
# 绘制历史数据
plt.plot(years, output_values, marker='o', label='历史数据', color='blue')
# 绘制线性回归直线
plt.plot(x_line, y_line, linestyle='--', color='green', label='线性回归趋势')
# 绘制预测点
plt.scatter(target_year, predicted_output, marker='x', color='red', label='2035 年预测值')

# 添加图标题和轴标签
plt.title('林业总产值随年份变化趋势')
plt.xlabel('年份')
plt.xticks(rotation=45)
plt.ylabel('林业总产值(亿元)')

# 添加图例
plt.legend()

# 显示网格线
plt.grid(True)

# 调整子图边距
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.2, top=0.9)

# 显示图形
plt.show()
