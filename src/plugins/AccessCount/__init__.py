# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.AccessCount
    ~~~~~~~~~~~~~~

    PV and IP plugins for statistical access.

    :copyright: (c) 2017 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from libs.base import PluginBase
import datetime
from config import PLUGINS
from .util import Click2MySQL, Click2Redis

__name__        = "AccessCount"
__description__ = "IP、PV统计插件"
__author__      = "Mr.tao"
__version__     = "0.1" 
__license__     = "MIT"
if PLUGINS["AccessCount"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"

def getPluginClass():
    return AccessCount

class AccessCount(PluginBase):
    """ 记录与统计每天访问数据 """

    @property
    def get_todayKey(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def Record_ip_pv(self, **kwargs):
        """ 记录ip、ip """

        data  = kwargs.get("access_data")
        pvKey = "EauDouce_PV_Statistics_" + self.get_todayKey
        ipKey = "EauDouce_IP_Statistics_" + self.get_todayKey
        '''
        try:
            self.redis.incr(pvKey)
            self.redis.sadd(ipKey, data.get("ip"))
        except Exception,e:
            self.logger.error(e, exc_info=True)
        else:
            return True
        '''
        self.asyncQueue.enqueue(Click2Redis, self.redis, data, pvKey, ipKey)
        self.asyncQueue.enqueue(Click2MySQL, self.mysql_write, data)

    def register_cep(self):
        return {"after_request_hook": self.Record_ip_pv}
