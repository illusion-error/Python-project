# TODO 导入生成随机数的模块
import random

# TODO 程序设定生成 1-30 之间的一个随机数并赋值给secretNum，让用户猜
secretNum = random.randint(1,30)

# 输出"这是一个位于1-30之间的数"
print("这是一个位于 1-30 之间的数")

# 设定用户只能猜 3 次
for number in range(1,4):
    # TODO 使用input()函数，请用户输入猜测的数，并使用int()函数取整
    # TODO 将输出的内容赋值给变量guess 
    guess = int(input("请输入猜测的数:"))
    # 当猜测结果小于等于0,或者大于30时，跳出
    if guess <= 0 or guess > 30:
        break
    # TODO 当猜测结果小于secretNum，输出"太小啦"  
    elif guess < secretNum:
        print("太小啦" )
    # TODO 继续判断，当猜测结果大于secretNum，输出"太大啦"    
    elif guess > secretNum:
        print("太大啦")
    # 其他情况跳出  
    else:
        break
# TODO 判断当猜测的结果与secretNum相同时，输出"真厉害，猜对啦"       
if guess == secretNum:
    print("真厉害，猜对啦")
# 其他情况，输出"很遗憾没有猜对，再玩一次吧"    
else:
    print("很遗憾没有猜对，再玩一次吧")
