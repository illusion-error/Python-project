import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# 读取 Excel 文件
file_path = r"D:/HuaweiMoveData/Users/符雨晗/Desktop/整理后数据/孔夫子旧书网 全部数据.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

# 提取“标题”列数据
titles = df['标题']

# 过滤掉非字符串类型的数据，将其转换为字符串
valid_titles = []
for title in titles:
    if isinstance(title, str):
        valid_titles.append(title)
    else:
        valid_titles.append(str(title))

# 将所有标题连接成一个字符串
text = ' '.join(valid_titles)

# 进行中文分词（如果是中文数据）
words = jieba.lcut(text)

# 加载停用词表，假设停用词表文件名为 stopwords.txt，每行一个停用词
with open(r"D:\HuaweiMoveData\Users\符雨晗\Desktop\stopwords.txt", 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

# 过滤停用词
filtered_words = [word for word in words if word not in stopwords and word.strip()]

# 统计词频
word_counts = Counter(filtered_words)

# 选取前十个高频词
top_ten_words = dict(word_counts.most_common(90))

# 创建词云对象
wordcloud = WordCloud(
    font_path='simhei.ttf',  # 中文字体路径，确保能正常显示中文
    background_color='white',  # 背景颜色
    width=800,  # 词云图宽度
    height=600  # 词云图高度
).generate_from_frequencies(top_ten_words)

# 显示词云图
plt.figure(figsize=(8, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
