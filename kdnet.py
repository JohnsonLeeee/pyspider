#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-01-27 01:18:31
# Project: kdnet

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

    def is_user_exist(self, username):
        db = self.db
        try:
            SQL = "select id from user where name = '{}'".format(username)
            with db.cursor() as cursor:
                rows = cursor.execute(SQL)
            db.commit()
            if rows > 0:
                return True
            else:
                return False

        except Exception as e:
            print("is_user_exist出错", e)
            self.db.rollback()

        return False

    def get_user_id_by_name(self, username):
        db = self.db
        try:
            SQL = "select id from user where name = '{}'".format(username)
            with db.cursor() as cursor:
                rows = cursor.execute(SQL)
                uid = cursor.fetchone()[0]
            db.commit()
            return uid

        except Exception as e:
            print("get_user_id_by_name出错", e)
            self.db.rollback()
        return 0

    def add_question(self, title, content, username):
        db = self.db
        if self.is_user_exist(username):
            user_id = self.get_user_id_by_name(username)
        else:
            user_id = random.randint(1, 10)
        print(user_id)
        try:
            SQL = 'INSERT INTO question(title, content, user_id, created_date, comment_count) values ("{title}", "{content}", {user_id}, now(), 0)'.format(
                title=title, content=content, user_id=user_id)
            # print(SQL)

            with db.cursor() as cursor:
                cursor.execute(SQL)  # 使用 execute()  方法执行 SQL
                qid = cursor.lastrowid

            # print(qid)
            db.commit()
            return qid
        except Exception as e:
            print("add_question出错", e)
            db.rollback()
        return 0

    def add_comment(self, comment, qid, user_name):
        db = self.db
        user_id = self.get_user_id_by_name(user_name)
        try:
            SQL = 'INSERT INTO comment(content, entity_type, entity_id, user_id, created_date) values ("{content}", "{entity_type}", {entity_id},{user_id}, now())'.format(
                content=comment, entity_type=1, entity_id=qid, user_id=user_id)
            # print(SQL)

            with db.cursor() as cursor:
                cursor.execute(SQL)  # 使用 execute()  方法执行 SQL

            # print(cursor.lastrowid)
            db.commit()
        except Exception as e:
            print('add_comment出错', e)
            db.rollback()

    def add_user(self, username):
        db = self.db
        head_url = "http://images.nowcoder.com/head/{}t.png".format(random.randint(1, 999))
        try:
            SQL = 'INSERT INTO user(name, password, head_url) values ("{name}", "{password}", "{head_url}")'.format(
                name=username, password=1, head_url=head_url)
            # print(SQL)

            with db.cursor() as cursor:
                cursor.execute(SQL)  # 使用 execute()  方法执行 SQL

            # print(cursor.lastrowid)
            db.commit()
        except Exception as e:
            print('add_user出错', e)
            db.rollback()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://club.kdnet.net/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div.hotplate a[href^="http://club.kdnet.net/list.asp?boardid="]').items():
            self.crawl(each.attr.href, callback=self.hotplate_page)

    @config(age=10 * 24 * 60 * 60)
    def hotplate_page(self, response):
        for each in response.doc('a[href^="http://club.kdnet.net/dispbbs.asp?id="]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        for each in response.doc('a[href^="http://club.kdnet.net/dispbbs.asp?id="]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        # 把所有的user存入user表
        user_names = response.doc('a[href^="http://user.kdnet.net/index.asp?userid="]').items()
        for each in user_names:
            user_name = each.text()
            if self.is_user_exist(user_name):
                continue
            else:
                self.add_user(each.text())

        # 把问题存入question表
        title = response.doc('div.posts-title').text()
        # print("title;", title)
        content = response.doc('div.posts-cont').html().replace('"', '\\"')
        # print("content:", content)
        qname = response.doc('div.posts-posted a[href^="http://user.kdnet.net/index.asp?userid="]').text()
        # print("qname:", qname)
        qid = self.add_question(title, content, qname)

        # 把评论存入comment表
        items = response.doc('div.reply-box').items()
        for each in items:
            # 获取PyQuery对象
            pq = each('div.replycont-text')
            # 去除引用框
            pq('span').remove()
            # 获取comment的内容
            comment = pq('div.replycont-text').text()
            if not comment:
                continue
            # 获取comment的发帖人姓名
            cname = each('span.name.c-main>a').text()

            self.add_comment(comment, qid, cname)

        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }


