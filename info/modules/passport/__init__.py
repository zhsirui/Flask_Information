#登陆注册的相关逻辑


from flask import Blueprint


passport_blu = Blueprint("passport", __name__, url_prefix="/passport")

from . import views