import numpy as np
from sklearn.linear_model import LinearRegression

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
