# Python 项目合集

这是一个 Python 学习与实践项目合集，包含基础语法练习、小游戏、数据库连接、自然语言处理、数据分析、机器学习建模、词云图和可视化图表等内容。项目适合作为 Python 入门学习记录，也可以作为课程作业、简历项目和后续整理优化的基础仓库。

## 项目目录

```text
Python-project/
└── Python项目/
    ├── 猜数字游戏.py
    ├── 人生模拟器.py
    ├── LOVE YOU.py
    ├── 数据库.py
    ├── py调用数据库1.py
    ├── 自然语言处理模型（已完成）.py
    ├── 提取书名.py
    ├── yequ.message.py
    ├── RFM/
    │   ├── RFM.py
    │   └── new_user_info.csv
    ├── py数据分析代码/
    │   ├── pd.read_csv.py
    │   ├── 价格销量.py
    │   ├── 多文件词云图.py
    │   ├── 林业线性回归折线图.py
    │   ├── 格兰检验.py
    │   ├── 直方图.py
    │   ├── 线性回归.py
    │   ├── 苗木价格弹性.py
    │   ├── 词云图.py
    │   ├── 黄花梨实体分析.py
    │   ├── stopwords.txt
    │   └── 图/
    ├── py速查表.pdf
    ├── 简历.zip
    ├── 放风筝商城html.zip
    └── 俄罗斯方块.rar
```

## 项目分类说明

| 分类 | 文件/目录 | 说明 |
| --- | --- | --- |
| 基础练习 | `猜数字游戏.py`、`人生模拟器.py`、`LOVE YOU.py` | 练习 Python 基础语法、条件判断、循环、输入输出和 turtle 绘图。 |
| 数据库操作 | `数据库.py`、`py调用数据库1.py` | 练习 MySQL 数据库连接、SQL 执行和查询结果读取。 |
| 文本处理与 NLP | `自然语言处理模型（已完成）.py`、`提取书名.py`、`yequ.message.py` | 练习文本处理、信息提取、邮件发送和自然语言处理接口调用。 |
| RFM 用户分析 | `RFM/RFM.py`、`RFM/new_user_info.csv` | 使用 RFM 指标和 KMeans 聚类进行用户价值分层。 |
| 数据分析与可视化 | `py数据分析代码/` | 包含 Excel/CSV 读取、价格销量分析、线性回归、格兰杰因果检验、词云图、价格弹性分析等脚本。 |
| 图表结果 | `py数据分析代码/图/` | 保存部分数据分析脚本生成的可视化图片。 |
| 学习资料与压缩包 | `py速查表.pdf`、`简历.zip`、`放风筝商城html.zip`、`俄罗斯方块.rar` | 保存课程资料、网页项目或其他历史练习文件。 |

## 运行方式

1. 克隆仓库

```bash
git clone https://github.com/illusion-error/Python-project.git
cd Python-project/Python项目
```

2. 运行单个 Python 文件

```bash
python 猜数字游戏.py
```

如果文件名包含中文或空格，建议使用支持 UTF-8 的终端，例如 PowerShell、Windows Terminal 或 VS Code 终端。

3. 数据分析脚本常用依赖

部分脚本需要安装第三方库：

```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels jieba wordcloud openpyxl pymysql requests tqdm
```

## 重点项目说明

### 1. RFM 用户价值分析

位置：`Python项目/RFM/RFM.py`

该脚本读取用户数据，提取 `time_gap`、`order_count`、`total_amount` 等特征，使用标准化和 KMeans 聚类对用户进行分群，可用于电商用户价值分析、客户运营分层等场景。

### 2. 数据分析与可视化脚本

位置：`Python项目/py数据分析代码/`

该目录包含多个数据分析任务：

- 价格与销量关系分析。
- 苗木价格弹性分析。
- 林业产值线性回归预测。
- 政策文本与林业产值的格兰杰因果检验。
- 商品标题词云图生成。
- Excel 多文件合并与清洗。

### 3. Python 基础小游戏

位置：`Python项目/猜数字游戏.py`、`Python项目/人生模拟器.py`

适合展示 Python 基础语法、流程控制、随机数、用户输入和简单交互逻辑。

## 注意事项

- 部分脚本使用了本地电脑中的绝对路径，运行前需要把路径改成自己电脑上的文件路径。
- 部分脚本依赖 Excel、CSV、图片或数据库环境，如果缺少数据文件，需要先准备对应数据。
- 数据库相关脚本需要本地 MySQL 服务，并根据自己的数据库地址、用户名、密码和表名进行修改。
- 项目中部分文件属于历史学习记录，代码风格和目录结构可以继续优化。
- 正式公开项目时，建议不要在代码中保存个人账号、密码、API Key 等敏感信息，应改用环境变量或配置文件。

## 建议优化方向

- 新增统一的 `requirements.txt`，方便一键安装依赖。
- 按照 `basic/`、`database/`、`nlp/`、`data_analysis/`、`machine_learning/` 重新整理目录。
- 为每个重点脚本补充输入数据说明、运行截图和输出示例。
- 将本地绝对路径改成相对路径，提升项目可复现性。
- 为数据分析项目补充 Jupyter Notebook 版本，方便展示分析过程。
- 把图表输出统一保存到 `outputs/` 目录，便于查看结果。

## 适合展示的能力

- Python 基础编程能力。
- 数据读取、清洗、分析和可视化能力。
- 机器学习基础建模能力。
- 数据库连接与 SQL 查询能力。
- 文本处理、词云图和 NLP 接口调用能力。
- 将学习练习逐步整理为可展示项目的工程化意识。
