# -*- coding: utf8 -*-
# 
# Base class: dependent services, connection information, and public information
#

from config import REDIS, MYSQL, PLUGINS
from torndb import Connection
from utils.tool import logger, ParseRedis, ParseMySQL


class ServiceBase(object):


    def __init__(self):

        #解析redis配置信息
        self._info   = ParseRedis(REDIS)
        #设置全局超时时间(如连接超时)
        self.timeout = 2
        #建立redis单机或集群连接
        if isinstance(self._info, dict):
            from redis import Redis
            self.redis = Redis(host=self._info.get("host", "localhost"), port=self._info.get("port", 6379), db=self._info.get("db", 0), password=self._info.get("password", None), socket_timeout=self.timeout)
        else:
            from rediscluster import StrictRedisCluster
            self.redis = StrictRedisCluster(startup_nodes=self._info, decode_responses=True, socket_timeout=self.timeout)
        #解析mysql配置并建立读写分离连接
        self._mysql = Connection(
                    host     = "%s:%s" %(ParseMySQL(MYSQL).get('Host', '127.0.0.1'), ParseMySQL(MYSQL).get('Port', 3306)),
                    user     = ParseMySQL(MYSQL).get('User', 'root'),
                    password = ParseMySQL(MYSQL).get('Password'),
                    database = ParseMySQL(MYSQL).get('Database'),
                    time_zone= ParseMySQL(MYSQL).get('Timezone','+8:00'),
                    charset  = ParseMySQL(MYSQL).get('Charset', 'utf8'),
                    connect_timeout=self.timeout,
                    max_idle_time=self.timeout)
        self.mysql_read = self._mysql
        self.mysql_write= self._mysql

