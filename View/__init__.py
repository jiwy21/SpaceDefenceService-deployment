# -*- coding:utf-8 -*-

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object('config')


from View import index
from View import service_view















