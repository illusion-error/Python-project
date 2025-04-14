# 导入pymysql模块
import pymysql

# 创建连接对象存储在变量conn中，并配置服务器地址、端口、用户名、密码与数据库名称
conn = pymysql.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "root",
    password = "lxfe0606",
    database ='nocturneshop')

# TODO 创建游标并存储在 cur 变量中
cur = conn.cursor()

# TODO 存储SQL指令 SELECT * FROM brand;
SQL = '''
SELECT *
FROM db;
'''



# TODO 执行SQL语句并存储在 ret 变量中
ret = cur.execute(SQL)
# TODO 输出 "本次查询共获得了{ret}条信息"
print(f"本次查询共获得了{ret}条信息")


# TODO 获取一条数据存储在 data1 中
data1 = cur.fetchone()
# TODO 输出 data1
print(data1)

# TODO 再获取4条数据存储在 data2 中
data2 = cur.fetchmany(4)
# TODO 输出 data2
print(data2)

# TODO 获取剩下所有数据存储在 data3 中
data3 = cur.fetchall()
# TODO 输出 data3
print(data3)


# TODO 关闭游标
cur.close

# 关闭连接
conn.close()
