# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.AccessCount
    ~~~~~~~~~~~~~~

    PV and IP plugins for statistical access.

    :copyright: (c) 2017 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

__name__        = "AccessCount"
__description__ = "PV and IP plugins for statistical access."
__author__      = "taochengwei"
__version__     = "0.1" 
__license__     = "MIT"
__license_file__= "LICENSE"
__readme_file__ = "README"


import requests, datetime
from libs.base import PluginBase


def getPluginClass():
    return "AccessCountPluginManager"


class AccessCountPluginManager(PluginBase):
    """ 记录与统计每天访问数据 """

    @property
    def get_todayKey(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def Record_ip_pv(self, ip):
        """ 记录ip、ip """

        self.pvKey = "EauDouce_PV_Statistics_" + self.get_todayKey
        self.ipKey = "EauDouce_IP_Statistics_" + self.get_todayKey
        try:
            self.redis.incr(self.pvKey)
            self.redis.sadd(self.ipKey, ip)
        except Exception,e:
            self.logger.error(e, exc_info=True)
        else:
            return True

    def run(self):
        """ 运行插件入口 """
        self.logger.info("I am AccessCount, {0} run!".format(getPluginClass()))
