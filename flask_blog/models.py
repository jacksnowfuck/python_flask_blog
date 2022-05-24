#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flask_blog import db


class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

class Comment(db.Model):  # 表名将会是 comment
    id = db.Column(db.Integer, primary_key=True)  # 主键
    user = db.Column(db.String(20))  # 昵称
    comment = db.Column(db.String(600))  # 评论内容
    add_time = db.Column(db.DateTime, default=datetime.now)  # 评论时间