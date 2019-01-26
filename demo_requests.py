# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 18:13
# @Author  : Li Shuai
# @FileName: demo_requests.py
# @Software: PyCharm

import requests

'''Session()会话对象
会话对象让你能够跨请求保持某些参数。
它也会在同一个 Session 实例发出的所有请求之间保持 cookie
会话对象具有主要的 Requests API 的所有方法。'''
payload = {'username': '李帅', 'password': '1'}
s = requests.Session()
content = s.get("http://localhost:8080/user/12").content.decode('utf-8')
print(content)

s.post("http://localhost:8080/login/", data=payload)
content = s.get("http://localhost:8080/user/12").content.decode('utf-8')
print(content)

s.get("http:localhost:8080/user/13", cookies={"ticket": "ac4740dad4d64b5083d6bb18ed5709be"})

stra = 'fdfaf'

stra.find('fd')