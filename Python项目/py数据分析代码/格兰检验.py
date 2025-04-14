import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
from statsmodels.tsa.api import VAR

# ======================
# 1. 数据加载与预处理（增强版）
# ======================

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

# 加载林业产值数据
forest_gdp = pd.read_excel(r"D:\HuaweiMoveData\Users\符雨晗\Desktop\先吃饭县\数据集合\国家林业产值.xlsx")
forest_gdp['年份'] = pd.to_datetime(forest_gdp['年份'], format='%Y')
forest_gdp.set_index('年份', inplace=True)

# 加载政策文件数据（带异常处理）
try:
    policy = pd.read_excel(r"D:/HuaweiMoveData/Users/符雨晗/Desktop/海南省林业局-部门政策文件.xlsx")
    print("政策文件加载成功，共加载政策条目：", len(policy))
except Exception as e:
    print(f"政策文件加载失败：{str(e)}")
    exit()

# ======================
# 2. 增强型政策变量生成
# ======================

# 定义关键词筛选条件（扩展列表）
keywords = [
    '林权制度', '林下经济', '林草种子', '林木流转',
    '国家公园', '热带雨林', '林木采伐', '林地利用',
    '一树一证', '林长制', '集体林权', '林下经济'
]

# 生成政策日期列表（带格式验证）
policy_dates = []
for idx, row in policy.iterrows():
    try:
        if any(kw in row['文件名'] for kw in keywords):
            date = pd.to_datetime(row['发布时间'])
            policy_dates.append(date.date())  # 转换为date类型避免时间戳问题
    except Exception as e:
        print(f"跳过无效日期格式：{row['发布时间']}，错误：{str(e)}")

# 创建政策虚拟变量（增强逻辑）
policy_series = pd.Series(0, index=forest_gdp.index)
if len(policy_dates) == 0:
    print("警告：未匹配到有效政策条目，请检查关键词设置！")
    exit()

# 标记政策实施后的年份
for date in policy_dates:
    year = pd.to_datetime(date).year
    policy_series.loc[policy_series.index >= f"{year}-01-01"] += 1

# 二值化处理（存在政策影响=1，无影响=0）
policy_series = (policy_series > 0).astype(int)

# 检查政策变量有效性
if policy_series.nunique() == 1:
    print("错误：政策虚拟变量无变化（全为0或全为1），请调整政策筛选条件！")
    exit()

# ======================
# 3. 数据平稳性处理（自动差分）
# ======================

# 合并数据
combined = pd.concat([
    forest_gdp['林业总产值(亿元)'],
    policy_series.rename('政策虚拟')
], axis=1).dropna()

# 自动差分函数
def auto_diff(series, max_diff=2):
    for i in range(1, max_diff+1):
        diff_series = series.diff(i).dropna()
        p_value = adfuller(diff_series)[1]
        if p_value < 0.05:
            return diff_series, i
    return None, None

# 对非平稳序列自动差分
print("\n林业产值平稳性检验:")
gdp_diff, gdp_diff_order = auto_diff(combined['林业总产值(亿元)'])
if gdp_diff is None:
    print("警告：林业产值序列无法通过差分达到平稳")
    exit()
else:
    combined['林业总产值_diff'] = gdp_diff
    print(f"林业产值经过{gdp_diff_order}阶差分后平稳")

# 检查政策变量平稳性（跳过差分处理）
print("\n政策变量平稳性检验:")
policy_pvalue = adfuller(combined['政策虚拟'])[1]
if policy_pvalue < 0.05:
    print("政策虚拟变量已平稳")
else:
    print(f"警告：政策虚拟变量非平稳（p={policy_pvalue:.4f}），但虚拟变量通常不进行差分")

# ======================
# 4. 格兰杰因果检验（稳健版）
# ======================

# 准备VAR模型数据
var_data = combined[['林业总产值_diff', '政策虚拟']].dropna()

# 自动选择最优滞后期（带异常处理）
try:
    model = VAR(var_data)
    results = model.fit(maxlags=3, ic='aic')
    optimal_lag = results.k_ar
except Exception as e:
    print(f"VAR模型拟合失败：{str(e)}")
    optimal_lag = 1  # 默认使用1阶滞后

# 执行格兰杰因果检验（带稳健性检查）
print("\n格兰杰因果检验结果：")
try:
    granger_results = grangercausalitytests(var_data, maxlag=optimal_lag, verbose=True)
except Exception as e:
    print(f"格兰杰检验失败：{str(e)}")
    exit()

# ======================
# 5. 可视化增强（带动态标注）
# ======================

plt.figure(figsize=(14, 10))

# 主图：林业产值与政策实施
ax1 = plt.subplot(211)
ax1.plot(combined.index, combined['林业总产值(亿元)'], 
        marker='o', color='#1f77b4', linewidth=2, label='原始数据')
ax1.plot(combined.index, combined['林业总产值(亿元)'].rolling(3).mean(),
        color='#ff7f0e', linestyle='--', label='三年移动平均')
ax1.set_title('海南省林业总产值趋势（2014-2023）', fontsize=14)
ax1.set_ylabel('总产值（亿元）', fontsize=12)
ax1.legend()
ax1.grid(alpha=0.3)

# 政策标注（带悬浮效果）
policy_years = list(set([d.year for d in policy_dates]))  # 去重年份
for year in policy_years:
    ax1.axvline(pd.to_datetime(f"{year}-01-01"), 
               color='#2ca02c', linestyle=':', alpha=0.7)
    ax1.text(pd.to_datetime(f"{year}-06-30"), ax1.get_ylim()[1]*0.95,
            f"{year}年政策实施",
            rotation=90, color='#2ca02c', ha='right', va='top',
            bbox=dict(facecolor='white', alpha=0.8))

# 差分序列图
ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(var_data.index, var_data['林业总产值_diff'], 
        color='#d62728', linewidth=1.5, label='差分后序列')
ax2.axhline(0, color='gray', linestyle='--')
ax2.set_title('林业产值差分序列（平稳化处理）', fontsize=14)
ax2.set_ylabel('产值变化量', fontsize=12)
ax2.legend()
ax2.grid(alpha=0.3)

# 日期格式化
years = mdates.YearLocator()
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig(r'D:\policy_impact_analysis_enhanced.png', dpi=300, bbox_inches='tight')
plt.show()

# ======================
# 6. 结果解读模板（增强版）
# ======================
'''
分析报告摘要：

1. 数据处理：
   - 林业产值序列经过{gdp_diff_order}阶差分后平稳（ADF p值：{adfuller(gdp_diff)[1]:.4f})
   - 共识别到有效政策条目：{len(policy_dates)}个
   - 政策影响时段：{policy_series.idxmax().year}年至今

2. 格兰杰因果检验：
   最优滞后期：{optimal_lag}
   主要检验指标（滞后期{optimal_lag}）：
   - F统计量：{granger_results[optimal_lag][0]['ssr_ftest'][0]:.2f}
   - P值：{granger_results[optimal_lag][0]['ssr_ftest'][1]:.4f}

3. 结论建议：
   { "政策影响显著" if granger_results[optimal_lag][0]['ssr_ftest'][1] < 0.05 else "未发现显著影响"}
'''
