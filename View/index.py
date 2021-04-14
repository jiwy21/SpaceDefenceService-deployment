
# -*- coding:utf-8 -*-

from View import app
from flask import render_template


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    return index list, it is just a demo for flask template render mechanism
    :return:
    """
    return render_template("index.html", title='Welcome to Service Market',
                           service_list={'id': 'ssss', 'name': 'sssss'})













