# 导入pandas模块，简称pd
import pandas as pd

'''读取数据集并获取特征变量'''
# 读取文件，并赋值给变量df
df = pd.read_csv(r"D:\HuaweiMoveData\Users\符雨晗\Desktop\new_user_info.csv")

# 获取特征变量x
x = df[["time_gap","order_count","total_amount"]]

'''数据归一化'''
# 导入sklearn.preprocessing模块中的StandardScaler类
from sklearn.preprocessing import StandardScaler

# 创建一个StandardScaler对象
scaler = StandardScaler()

# 对x进行归一化
x_scale = scaler.fit_transform(x)

'''进行KMeans算法的聚类运算'''
# 导入sklearn.cluster模块中的KMeans模型
from sklearn.cluster import KMeans

# 使用KMeans()初始化模型
# 设置参数n_clusters=3, random_state=1
# 将结果赋值给model
model = KMeans(n_clusters=3, random_state=1)
    
# 使用fit()函数训练模型
model.fit(x_scale)

# 获取每个样本所属的簇
labels = model.labels_

'''可视化结果'''
# 导入matplotlib.pyplot，并使用"plt"作为该模块的简写
import matplotlib.pyplot as plt

# 从mpl_toolkits.mplot3d中导入Axes3D类
from mpl_toolkits.mplot3d import Axes3D

# 通过 rcParams 参数将字体设置为 SimHei
plt.rcParams["font.sans-serif"] = "SimHei"

# 使用plt.figure()函数创建画布
# 添加参数figsize设置画布大小为(12,8)
fig = plt.figure(figsize=(12,8))

# 创建3D坐标轴对象
ax = fig.add_subplot(projection="3d")

# 设置散点颜色
color = ["dodgerblue", "seagreen", "lightcoral"]

# 遍历三个簇
for i in range(0,3):
    
    # 获取分类为i的点
    d = x[labels == i]
    
    # 绘制分类为i的簇所对应的R、F和M这三个指标数据
    ax.scatter(d["time_gap"], d["order_count"], d["total_amount"], color=color[i], label=f"用户群体{i}")

# 设置x轴标题为"R"
ax.set_xlabel("R")
# 设置y轴标题为"F"
ax.set_ylabel("F")
# 设置z轴标题为"M"
ax.set_zlabel("M")

# 使用plt.legend()函数展示图例
plt.legend()
# 展示图像
plt.show()
