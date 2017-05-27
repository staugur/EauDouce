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

__name__        = "AccessCount"
__description__ = "IP、PV统计插件"
__author__      = "Mr.tao"
__version__     = "0.1" 
__license__     = "MIT"


def getPluginClass():
    return AccessCount

class AccessCount(PluginBase):
    """ 记录与统计每天访问数据 """

    @property
    def get_todayKey(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def Record_ip_pv(self, **kwargs):
        """ 记录ip、ip """

        request    = kwargs.get("request")
        ip         = request.headers.get('X-Real-Ip', request.remote_addr)
        self.pvKey = "EauDouce_PV_Statistics_" + self.get_todayKey
        self.ipKey = "EauDouce_IP_Statistics_" + self.get_todayKey
        try:
            self.redis.incr(self.pvKey)
            self.redis.sadd(self.ipKey, ip)
        except Exception,e:
            self.logger.error(e, exc_info=True)
        else:
            return True

    def register_cep(self):
        return {"before_request_hook": self.Record_ip_pv}
