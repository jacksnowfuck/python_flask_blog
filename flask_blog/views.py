#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import markdown
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user

from flask_blog import app, db
from flask_blog.models import User, Article, Comment

@app.route('/', methods=['GET','POST'])
def index():
    articles = Article.query.all()
    comments = Comment.query.all()
    return render_template('index.html', articles=articles, comments=comments)

@app.route('/article/<int:article_id>', methods=['GET','POST'])
def details(article_id):
    if request.method == 'POST':
        content = request.form.get('content')
        comment_user = request.form.get('comment_user')
        if not content or not comment_user or len(comment_user) > 20 or len(content) > 500:
            flash('请认真填写')
            return redirect(url_for('index'))
        if content and comment_user:
            comment = Comment(comment_user=comment_user, content=content, article_id=article_id)
            db.session.add(comment)
            db.session.commit()
        flash('创建成功')
        return redirect(url_for('details', article_id=article_id))
    article = Article.query.get_or_404(article_id)
    comments = Comment.query.filter_by(article_id=article_id).all()
    return render_template('details.html', article=article, comments=comments)

@app.route('/article/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = Article.query.get_or_404(article_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        id = request.form['id']
        if not title or not content or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('edit', article_id=article_id))  # 重定向回主页

        article.title = title
        article.content = content
        article.id = id
        db.session.commit()
        flash('条例更新完成')
        return redirect(url_for('admin'))

    return render_template('edit.html', article=article)

@app.route('/article/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('删除条例')
    return redirect(url_for('admin'))

@app.route('/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论')
    return redirect(url_for('admin'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.first()
        print(user)
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功')
            return redirect((url_for('admin')))

        flash('认证失败')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('不对劲')
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    articles = Article.query.all()
    comments = Comment.query.all()
    return render_template('admin.html',articles=articles, comments=comments)

@app.route('/admin/add', methods=['GET','POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        id = request.form.get('id')
        if title and content:
            article = Article(title=title, content=content, id=id)
            db.session.add(article)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('admin'))
    return render_template('add.html')