# -*- coding: utf8 -*-

import requests
from libs.base import PluginBase
from utils.tool import get_todayKey, plugin_logger

def getPluginClass():
    return AccessCountPluginManager

class AccessCountPluginManager(PluginBase):
    """ 记录与统计每天访问数据 """

    def __init__(self):
        super(AccessCountPluginManager, self).__init__()
        self.pvKey = "EauDouce_PV_Statistics_"+get_todayKey()
        self.ipKey = "EauDouce_IP_Statistics_"+get_todayKey()

    def Record_ip_pv(self, ip):
        """ 记录ip、ip """
        try:
            self.redis.incr(self.pvKey)
            self.redis.sadd(self.ipKey, ip)
        except Exception,e:
            plugin_logger.error(e, exc_info=True)
        else:
            return True

    def run(self):
        """ 运行插件入口 """
        plugin_logger.info("{0} run!".format(getPluginClass()))
