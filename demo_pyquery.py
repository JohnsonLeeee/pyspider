# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 20:57
# @Author  : Li Shuai
# @FileName: demo_pyquery.py
# @Software: PyCharm
# pyquery语法和jquery差不多
from pyquery import PyQuery as pq

q = pq(open("v2ex.html", encoding='utf-8').read())
print(1, q("title"))
print(2, q("title").html())
print(3, type(q))
print(3, type(q("title")))
# print(q('div.inner'))

# selector的使用:
# .表示选择class="inner"
# >表示p元素下的子节点a
# .items()的用法
# .attr()的用法
# .find()的用法
for each in q("div.inner>a").items():
    if (each.attr('href').find("tab")) > 0:
        print(4, each.attr('href'))

# #Tabs表示选择id="Tabs"
for each in q("div#Tabs>a").items():
    print(5, each.attr('href'))

# a[href^="/go"]表示超链接下,href中以/go开头的
for each in q('.cell>a[href^="/go"]').items():
    print(6, each.attr.href)

# 空格表示id="cell"的元素下的a[href^="/go"]元素（不必父子）
for each in q('.cell a[href^="/go"]').items():
    print(6, each.attr.href)
    print("中文")


for each in q('span.item_title>a').items():
    print(7, each.html())

q = pq('<div class="replycont-box clearfix"><div class="replycont-box-r"><div class="replycont-text" style="word-spacing: 2px;"><span class="quote-cont-box"><span class="quote-cont2"><span class="quote-title"><span><a href="http://club.kdnet.net/dispbbs.asp?boardid=1&amp;id=13152366&amp;replyid=81094316#81094316" onclick="return checkurl(this);">转至第7楼</a></span>第 7 楼 <a href="http://user.kdnet.net/index.asp?username=冷眼风云00001" target="_blank" onclick="return checkurl(this);">冷眼风云00001</a> 2019/1/26 11:32:38&nbsp;&nbsp;的原帖：</span>&nbsp;&nbsp;&nbsp;&nbsp;刚过去的“腊八节”，成千上万人一早排队等待“施粥”，可见中国还是穷人很多的----连稀饭都喝不起。</span></span>不是喝不起，而是传说每年到寺院吃布施的腊八弱会纳百家福，讨个意头而已，往年有空我也会去排队喝，还打包回家给家人分着吃一点。</div></div></div>')
q('span').remove()
print(1, q.text())

