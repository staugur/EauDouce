# -*- coding: utf-8 -*-
"""
    EauDouce.libs.cache
    ~~~~~~~~~~~~~~

    Cache class.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from .base import ServiceBase

class CacheManager(ServiceBase):


    def __init__(self):
        super(CacheManager, self).__init__()
        self.index = "EauDouce:cache"

    def setKey(self, key):
        return "{}_{}".format(self.index, key)

    def cacheIndex(self):
        
        sql  = "SELECT id,title,create_time,update_time,tag,author,catalog FROM blog_article"
        data = self.mysql_read.query(sql)

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
        data= self.mysql_read.get(sql)
        return self.redis.set(key, json.dumps(data))

    def get_cache_blog(self, blogId):
        key = self.setKey(blogId)
        if self.redis.exists(key):
            return json.loads(self.redis.get(key))
        else:
            return False
