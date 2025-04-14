# 从turtle中导入所有函数
from turtle import *

# 绘制心形
# 使用pensize()函数将画笔粗细设置为5
pensize(5)
# 使用pencolor()函数设置颜色
# 画笔颜色为"red"
pencolor("red")
# 使用fillcolor()函数设置填充颜色
# 填充颜色为"pink"
fillcolor("pink")
# 使用begin_fill()函数准备开始填充图形
begin_fill()
# 使用left()函数向左转135度
left(135)
# 使用forward()函数向前进100步
forward(100)
# 使用right()函数右转180度
right(180)
# 使用circle()函数画半圆，半径为50，角度-180度
circle(50,-180)
# 使用left()函数向左转90度
left(90)
# 使用circle()函数画半圆，半径为50，角度-180度
circle(50,-180)
# 使用right()函数右转180度
right(180)
# 使用forward()函数向前进100步
forward(100)
# 使用end_fill()函数填充完成
end_fill()

# 填充文字
# TODO 使用penup()函数抬起画笔
penup()
# 使用pencolor()函数设置画笔颜色为黑色
pencolor("black")
# 使用goto()函数将画笔移动到坐标(0,80)的位置
goto(0,80)
# TODO 使用hideturtle()函数隐藏画笔
hideturtle()
# 设定write()函数输入内容为"LOVE YOU"，居中对齐，字体为"Arial"和大小为20粗细为"bold'
write("LOVE YOU",align = "center",font=("Arial",20,"bold"))
