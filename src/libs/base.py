# -*- coding: utf-8 -*-
"""
    EauDouce.libs.base
    ~~~~~~~~~~~~~~

    Base class: dependent services, connection information, and public information.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from rq import Queue
from redis import from_url
from torndb import Connection
from config import REDIS, MYSQL, PLUGINS
from utils.tool import ParseMySQL, logger


class ServiceBase(object):
    """ 所有服务的基类 """

    def __init__(self):
        #设置全局超时时间(如连接超时)
        self.timeout= 2
        #建立redis单机或集群连接
        self.redis  = from_url(REDIS)
        #解析mysql配置并建立读写分离连接
        self._minfo = ParseMySQL(MYSQL)
        self._mysql = Connection(
                    host     = "%s:%s" %(self._minfo.get('Host', '127.0.0.1'), self._minfo.get('Port', 3306)),
                    user     = self._minfo.get('User', 'root'),
                    password = self._minfo.get('Password'),
                    database = self._minfo.get('Database'),
                    time_zone= self._minfo.get('Timezone','+8:00'),
                    charset  = self._minfo.get('Charset', 'utf8'),
                    connect_timeout=self.timeout,
                    max_idle_time=self.timeout)
        self.mysql_read = self._mysql
        self.mysql_write= self._mysql
        self.asyncQueue = Queue(connection=self.redis)
        self.asyncQueueLow = Queue(name='low', connection=self.redis)
        self.asyncQueueHigh = Queue(name='high', connection=self.redis)


class PluginBase(ServiceBase):
    """ 插件基类: 提供插件所需要的公共接口与扩展点 """
    
    def __init__(self):
        super(PluginBase, self).__init__()
        self.logger = logger.plugin
