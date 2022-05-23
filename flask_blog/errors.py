#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import render_template

from flask_blog import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404