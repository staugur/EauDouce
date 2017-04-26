# -*- coding: utf8 -*-
# Cache blog data

from redis import Redis
from config import REDIS
from utils.tool import logger


class BaseApiManager(object):


    def __init__(self):
        self.redis = Redis(host="127.0.0.1", port=16379, db=0, password="SaintIC")

        KEY  = "blog"
        sql  = "SELECT id,title,create_time,update_time,tag,author,catalog FROM blog_article"
        data = mysql.query(sql)

for blog in data:
    print blog.id, blog.title, blog.create_time, blog.update_time, blog.tag, blog.catalog, blog.author
    key = "%s_%d" %(KEY, blog.id)
    for k,v in blog.iteritems():
        if k == "id": continue
        redis.hset(key, k, v)
    redis.expire(key, 1200)

