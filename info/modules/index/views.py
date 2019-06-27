from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from info import constants
from info.models import User, News, Category
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import index_blu
from info import redis_store


@index_blu.route('/news_list')
def news_list():

    cid = request.args.get("cid", "1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")

    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    filters = [News.status == 0]
    if cid != 1:
        filters.append(News.category_id == cid)

    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询错误")

    news_model_list = paginate.items
    total_page = paginate.pages
    current_page = paginate.page

    news_dict_li = []
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())

    data = {
        "news_dict_li": news_dict_li,
        "total_page": total_page,
        "current_page": current_page
    }

    return jsonify(errno=RET.OK, errmsg="OK", data=data)


@index_blu.route('/')
@user_login_data
def index():

    user = g.user

    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())

    categories = Category.query.all()
    category_li = []
    for category in categories:
        category_li.append(category.to_dict())

    data = {
        "user": user.to_dict() if user else None,
        "news_dict_li": news_dict_li,
        "category_li": category_li
    }


    return render_template('news/index.html', data=data)


@index_blu.route('/favicon.ico')
def favcion():
    return current_app.send_static_file('news/favicon.ico')