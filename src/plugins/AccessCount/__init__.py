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
from config import PLUGINS
from utils.tool import get_today
from utils.qf import Click2MySQL, Click2Redis

__name__        = "AccessCount"
__description__ = "IP、PV、UV统计插件"
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

    pvKey = "EauDouce:AccessCount:pv:" + get_today("%Y%m%d")
    ipKey = "EauDouce:AccessCount:ip:" + get_today("%Y%m%d")
    urlKey= "EauDouce:AccessCount:uv"

    def Record_ip_pv(self, **kwargs):
        """ 记录ip、ip """

        data  = kwargs.get("access_data")
        self.asyncQueue.enqueue(Click2Redis, data, self.pvKey, self.ipKey, self.urlKey)
        self.asyncQueue.enqueue(Click2MySQL, data)

    def QueueUV(self, g, url):
        g.QueueUV = self.redis.hgetall(self.urlKey).get(url)
        self.logger.info(g.QueueUV)

    def register_cep(self):
        return {"after_request_hook": self.Record_ip_pv, "before_request_hook": lambda request,g:self.QueueUV(g, request.url)}

    def register_tep(self):
        """注册博客详情页功能区代码"""
        tep = {"blog_show_funcarea_string": '<i class="icon-eye-open icon-1x"></i><scan style="color: #999">&nbsp;{{ g.QueueUV }}</scan>&nbsp;'}
        return tep