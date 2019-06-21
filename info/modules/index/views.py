from flask import current_app
from flask import render_template
from . import index_blu
from info import redis_store


@index_blu.route('/')
def index():
    return render_template('news/index.html')


@index_blu.route('/favicon.ico')
def favcion():
    return current_app.send_static_file('news/favicon.ico')