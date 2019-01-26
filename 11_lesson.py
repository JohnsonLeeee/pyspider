import requests
from bs4 import BeautifulSoup


def qiushibaike():
    content = requests.get("https://www.qiushibaike.com/hot/").content
    soup = BeautifulSoup(content, 'html.parser')
    for div in soup.find_all('div', {'class' : 'content'}):
        print(div.text.strip())


# qiushibaike()


# 1. 字符串
def demo_str():
    a = 'hello world'
    print(1, a.capitalize())
    print(2, a.replace('l', "我是个好人", 2)) # 2表示替换2次l,第3个l就不替换了
    b = ' \n \r hello world, \n'
    print(3, b.lstrip())
    print(4, b.rstrip())
    print(5, b.strip())


demo_str()




def add(a, b):
    return a + b


def sub(a, b):
    return a - b


dict_A = {'+': add, '-': sub}    # 注意这里方法也可以放进dict里
A = dict_A['+'](2, 3)
print(A)


x = 3
B = eval('x+3')    # 注意这里eval的用法
print(B)


# set的用法
set_A = set([1, 2, 3, 4, 5])
set_B = set([3, 4, 5, 6, 7])
print(1, set_A - set_B)
print(1, set_A | set_B)
print(1, set_A & set_B)



