print("你好")
a = 1
b = 2
c = 3
print("this is a line with\n你知道吗")  # 反斜杠可以用来转义，使用 r 可以让反斜杠不发生转义。 如 r"this is a line with \n" 则 \n 会显示，并不是换行
print(r"this is a line with\n你知道吗")
print("http://baidu.com/" + "config")  # 字符串可以用 + 运算符连接在一起，用 * 运算符重复

"""字符串的截取的语法格式如下：变量[头下标:尾下标:步长]"""
str = '123456789'
print(str)  # 输出字符串
print(str[0:8])  # 输出第一个到倒数第二个的所有字符
print(str[0:-1])
print(str[0])  # 输出字符串第一个字符
print(str[2:5])  # 输出从第三个开始到第六个的字符（不包含）
print(str[2:])  # 输出从第三个开始后的所有字符
print(str[1:5:2])  # 输出从第二个开始到第五个且每隔一个的字符（步长为2）
print(str * 2)  # 输出字符串两次
print(str + "你好")  # 连接字符串
print('------------------------------')
print('hello\nrunoob')  # 使用反斜杠(\)+n转义特殊字符
print(r'hello\nrunoob')  # 在字符串前面添加一个 r，表示原始字符串，不会发生转义

"""这里的 r 指 raw，即 raw string，会自动将反斜杠转义，例如"""
print('\n')  # 输出空行
print(r'\n')  # 输出 \n

"""等待用户输入"""
# input("\n\n按下 enter 键后退出。")
"""以上代码中 ，\n\n 在结果输出前会输出两个新的空行。一旦用户按下 enter 键时，程序将退出。"""

"""
同一行显示多条语句
Python 可以在同一行中使用多条语句，语句之间使用分号 ; 分割，以下是一个简单的实例：
"""
import sys;

x = 'runoob';
sys.stdout.write(x + '\n')

"""
print 默认输出是换行的，如果要实现不换行需要在变量末尾加上 end=""：
"""

num1 = 1
num2 = 2
print(num1)
print(num2)
print("-------------------------")
a1 = "mu"
a2 = "xiaowen"
print(a1, end="")
print(a2)
print("-------------------------")

"""
import 与 from...import
"""
import sys

print('================Python import mode==========================')
print('命令行参数为:')
for i in sys.argv:
    print(i)
print('\n python 路径为', sys.path)

from sys import argv, path  # 导入特定的成员

print('================python from import===================================')
print('path:', path)  # 因为已经导入path成员，所以此处引用时不需要加sys.path

"""
多个变量赋值
"""
aa1, aa2, aa3 = 1, 2, "dadada"
print(type(aa1))
print(aa2)
print(type(aa3))

"""
Python3 的六个标准数据类型中：
不可变数据（3 个）：Number（数字）、String（字符串）、Tuple（元组）；
可变数据（3 个）：List（列表）、Dictionary（字典）、Set（集合）。
此外还有一些高级的数据类型，如: 字节数组类型(bytes)
内置的 type() 函数可以用来查询变量所指的对象类型
此外还可以用 isinstance 来判断
"""

#isinstance 来判断
ab = 100
isinstance(ab,int)

"""
String（字符串）
Python中的字符串用单引号 ' 或双引号 " 括起来，同时使用反斜杠 \ 转义特殊字符。
字符串的截取的语法格式如下：变量[头下标:尾下标]
索引值以 0 为开始值，-1 为从末尾的开始位置。
加号 + 是字符串的连接符， 星号 * 表示复制当前字符串，与之结合的数字为复制的次数。实例如下：
"""


def reverseWords(input):
    # 通过空格将字符串分隔符，把各个单词分隔为列表
    inputWords = input.split(" ")
    print(inputWords)

    # 翻转字符串
    # 假设列表 list = [1,2,3,4],
    # list[0]=1, list[1]=2 ，而 -1 表示最后一个元素 list[-1]=4 ( 与 list[3]=4 一样)
    # inputWords[-1::-1] 有三个参数
    # 第一个参数 -1 表示最后一个元素
    # 第二个参数为空，表示移动到列表末尾
    # 第三个参数为步长，-1 表示逆向
    inputWords = inputWords[-1::-1]
    print(inputWords)

    # 重新组合字符串
    output = ' '.join(inputWords)

    return output


if __name__ == "__main__":
    input = 'I like runoob'
    rw = reverseWords(input)
    print(rw)