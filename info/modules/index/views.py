from . import index_blu
from info import redis_store

@index_blu.route('/')
def index():

    return 'index'