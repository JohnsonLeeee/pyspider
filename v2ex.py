# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-01-25 17:53:04
# Project: v2ex

from pyspider.libs.base_handler import *
import pymysql
import random


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  passwd='159357',
                                  db='wenda',
                                  charset='utf8')

    def add_question(self, title, content):
        db = self.db
        user_id = random.randint(1, 10)
        try:
            SQL = 'INSERT INTO question(title, content, user_id, created_date, comment_count) values ("{title}", "{content}", {user_id}, now(), 0)'.format(title=title, content=content, user_id=user_id)
            # print(SQL)

            with db.cursor() as cursor:
                cursor.execute(SQL)  # 使用 execute()  方法执行 SQL

            print(cursor.lastrowid)
            db.commit()
        finally:
            db.close()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.v2ex.com/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div#Tabs>a[href^="https://www.v2ex.com/?tab="]').items():
            self.crawl(each.attr.href, callback=self.tab_page)

    @config(priority=2)
    def tab_page(self, response):
        for each in response.doc('div#SecondaryTabs>a[href^="https://www.v2ex.com/go"]').items():
            self.crawl(each.attr.href, callback=self.board_page)

    @config(priority=3)
    def board_page(self, response):
        for each in response.doc('a[href^="https://www.v2ex.com/t/"]').items():
            # 去重#reply意思是有多少回复,如果回复数改变,网址就变了
            url = each.attr.href
            index = url.find('#reply')
            print(type(url))
            if index > 0:
                url = url[:index]
            self.crawl(url, callback=self.detail_page)

        for each in response.doc('a.page_normal').items():
            self.crawl(each.attr.href, callback=self.board_page)

    @config(priority=4)
    def detail_page(self, response):
        title = response.doc('h1').text()
        content = response.doc('div.topic_content>div.markdown_body').text()
        # print(content)
        self.add_question(title, content)
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }


