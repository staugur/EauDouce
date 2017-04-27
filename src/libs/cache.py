# -*- coding: utf8 -*-
# Cache blog data

import json
from torndb import Connection
from config import REDIS, MYSQL
from utils.tool import logger, ParseRedis, ParseMySQL


class CacheManager(object):


    def __init__(self, timeout=5):
        self._info = ParseRedis(REDIS)
        self.index = "EauDouceBlog"
        if isinstance(self._info, dict):
            from redis import Redis
            self.redis = Redis(host=self._info.get("host", "localhost"), port=self._info.get("port", 6379), db=self._info.get("db", 0), password=self._info.get("password", None), socket_timeout=timeout)
        else:
            from rediscluster import StrictRedisCluster
            self.redis = StrictRedisCluster(startup_nodes=self._info, decode_responses=True, socket_timeout=timeout)
        self.mysql = Connection(
                    host     = "%s:%s" %(ParseMySQL(MYSQL).get('Host', '127.0.0.1'), ParseMySQL(MYSQL).get('Port', 3306)),
                    user     = ParseMySQL(MYSQL).get('User', 'root'),
                    password = ParseMySQL(MYSQL).get('Password'),
                    database = ParseMySQL(MYSQL).get('Database'),
                    time_zone= ParseMySQL(MYSQL).get('Timezone','+8:00'),
                    charset  = ParseMySQL(MYSQL).get('Charset', 'utf8'),
                    connect_timeout=3,
                    max_idle_time=2)

    def setKey(self, key):
        return "{}_{}".format(self.index, key)

    def cacheIndex(self):
        
        sql  = "SELECT id,title,create_time,update_time,tag,author,catalog FROM blog_article"
        data = self.mysql.query(sql)

        for blog in data:
            #print blog.id, blog.title, blog.create_time, blog.update_time, blog.tag, blog.catalog, blog.author
            key = "%s_%d" %(self.index, blog.id)
            for k,v in blog.iteritems():
                if k == "id": continue
                self.redis.hset(key, k, v)
            self.redis.expire(key, 1200)

    def post_cache_blog(self, blogId):
        key = self.setKey(blogId)
        sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author FROM blog_article WHERE id=%s" %blogId
        data= self.mysql.get(sql)
        return self.redis.set(key, json.dumps(data))
        #return self.redis.set(key, data)

    def get_cache_blog(self, blogId):
        key = self.setKey(blogId)
        return json.loads(self.redis.get(key))
        #return self.redis.get(key)
