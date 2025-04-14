# 导入csv模块
import csv
# 导入jieba模块
import jieba
# 从sklearn.feature_extraction.text中导入CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
# 从sklearn.model_selection中导入train_test_split
from sklearn.model_selection import train_test_split


'''1. 读取文件'''

# 使用open()函数打开csv文件，并赋值给变量file，
file = open(r"C:\Users\符雨晗\Desktop\python\练习文件\hotelComment.csv", "r", encoding="utf-8")

# 使用reader()函数读取file中的内容，并赋值给变量reader
reader = csv.reader(file)

# 使用list()函数将reader转化为列表，并赋值给变量data
data = list(reader)


'''2. 批量分词'''

# 创建一个空列表word
word = []

# 使用for循环遍历data，将遍历的数据存储到变量row中
for row in data:
    
    # 获取每行第一列数据 并赋值给变量text
    text = row[0]
    
    # 使用lcut()函数进行分词，并赋值给ret
    ret = jieba.lcut(text)
    
    # 将分词结果以空格合并为字符串，并存储在ret变量中
    ret = " ".join(ret)
    
    # 使用append()函数将分词结果添加到列表word中
    word.append(ret)


'''3.1 提取文本特征'''

# 创建CountVectorizer对象，并存储在vect中
vect = CountVectorizer()

# 使用fit_transform()函数，将word中的数据传递给vect，并赋值给变量X
X = vect.fit_transform(word)

# 使用toarray()函数，将X转换为数组
X = X.toarray()


'''3.2 提取标签'''

# 创建一个空列表y，用于存储标签
y=[]

# 使用for循环遍历data，将遍历的数据存储到变量allInfo中
for allInfo in data:
    
    # 获取每行第二列数据 并赋值给变量label
    label = allInfo[1]
    
    # 使用append()函数将label添加到列表y中
    y.append(label)


'''4. 划分数据集'''

# 划分数据集，将数据分为训练集和测试集
result = train_test_split(X, y, train_size=0.8, random_state=1)

# 依次提取result中训练集特征、测试集特征、训练集标签和测试集标签
train_feature = result[0]
test_feature = result[1]
train_label = result[2]
test_label = result[3]


'''5. 生成分类器模型'''

# TODO 从sklearn.neural_network中导入MLPClassifier
from sklearn.neural_network import MLPClassifier

# TODO 创建MLPClassifier对象，并存储在mlp变量中
mlp = MLPClassifier()

# TODO 使用fit()函数，通过train_feature和train_label，训练分类器
mlp.fit(train_feature,train_label)

'''6. 评估模型准确率'''

# TODO 从sklearn.metrics中导入accuracy_score
from sklearn.metrics import accuracy_score

# TODO 对测试集数据进行预测
text_pred = mlp.predict(test_feature)

# TODO 计算预测准确率，并将结果赋值给score
score = accuracy_score(text_pred,test_label)

# TODO 输出准确率
print(score)


'''7. 自定义评价，并预测'''

# TODO 自定义一条评价，并存储在变量comment中
comment = "隐私性不行"

# 使用jieba.lcut()对comment进行分词
comment = jieba.lcut(comment)
# 使用join()函数处理分词结果
comment =  [' '.join(comment)]
# 构造词袋模型
try_feature = vect.transform(comment)
# 使用toarray()函数把结果转换为NumPy数组
try_feature = try_feature.toarray()
# 使用predict()函数预测结果
try_pred = mlp.predict(try_feature)
# 输出预测结果
print(try_pred)
