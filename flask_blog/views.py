#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import or_, desc, func
from flask_blog import app, db
from flask_blog.models import User, Article, Comment

@app.route('/', methods=['GET','POST'])
def index():
    articles = Article.query.order_by(desc(Article.add_time)).all()
    comments = db.session.query(Comment.article_id, func.count(Comment.article_id)).group_by(Comment.article_id).all()
    page = request.args.get('page', 1, type=int)
    if page>len(articles) or page<1:
        page = 1
    current_page = Article.query.order_by(desc(Article.add_time)).paginate(page, per_page=8, error_out=False)
    ret = current_page.items
    return render_template('index.html', articles=ret, current_page=current_page, comments=comments)

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
    comments = Comment.query.filter_by(article_id=article_id).order_by(desc(Comment.add_time)).all()
    return render_template('details.html', article=article, comments=comments, article_id=str(article_id))

@app.route('/article/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = Article.query.get_or_404(article_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        id = request.form['id']
        category = request.form['category']
        if not title or not content or len(title) > 200:
            flash('输入不对劲')  # 显示错误提示
            return redirect(url_for('edit', article_id=article_id))  # 重定向回主页

        article.title = title
        article.content = content
        article.id = id
        article.category = category
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
    return redirect(request.referrer or url_for('admin'))

@app.route('/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论')
    return redirect(request.referrer or url_for('admin'))

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
    articles = Article.query.order_by(desc(Article.add_time)).all()
    comments = Comment.query.order_by(desc(Comment.add_time)).all()
    page = request.args.get('page', 1, type=int)
    if page>len(articles) or page<1:
        page = 1
    current_page = Article.query.order_by(desc(Article.add_time)).paginate(page, per_page=8)
    ret = current_page.items
    return render_template('admin.html', articles=ret, comments=comments, current_page=current_page)

@app.route('/admin/add', methods=['GET','POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        id = request.form.get('id')
        category = request.form.get('category')
        if title and content:
            article = Article(title=title, content=content, id=id, category=category)
            db.session.add(article)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('admin'))
    return render_template('add.html')

@app.route('/search', methods=['GET','POST'])
def search():
    keyword = request.args.get('keyword')
    result = Article.query.filter(or_(Article.title.contains(keyword),Article.content.contains(keyword))).order_by(desc(Article.add_time)).all()
    if result:
        return render_template('index.html', articles=result)
    else:
        flash('啥也没搜到')
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def list():
    articles = Article.query.all()
    return render_template('list.html', articles=articles)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/category/<category_name>', methods=['GET','POST'])
def category(category_name):
    articles = Article.query.filter_by(category=category_name).order_by(desc(Article.add_time)).all()
    return render_template('category.html', articles=articles, category=category_name)
