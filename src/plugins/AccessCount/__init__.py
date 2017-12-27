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
from utils.tool import get_today, getIpArea
from utils.qf import Click2MySQL, Click2Redis
from flask import Blueprint, jsonify, request

__name__        = "AccessCount"
__description__ = "IP、PV、UV统计插件"
__author__      = "Mr.tao"
__version__     = "0.1" 
__license__     = "MIT"
if PLUGINS["AccessCount"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"


pb    = PluginBase()
uvKey = "EauDouce:AccessCount:uv:hash"
AccessCountBlueprint = Blueprint("AccessCount", "AccessCount")
@AccessCountBlueprint.route("/uv/")
def uv():
    url = request.args.get("url")
    res = {"code": 0, "msg": None, "data": None, "url": url}
    sql = "SELECT count(id) FROM blog_clicklog WHERE url LIKE '%%{}%%'".format(url)
    res.update(data=pb.mysql_read.get(sql).get('count(id)'))
    pb.logger.info(res)
    return jsonify(res)

def getPluginClass():
    return AccessCount

class AccessCount(PluginBase):
    """ 记录与统计每天访问数据 """

    pvKey = "EauDouce:AccessCount:pv:hash"
    ipKey = "EauDouce:AccessCount:ip:" + get_today("%Y%m%d")
    urlKey= uvKey

    def Record_ip_pv(self, **kwargs):
        """ 记录ip、ip """
        data  = kwargs.get("access_data")
        self.asyncQueue.enqueue(Click2Redis, data, self.pvKey, self.ipKey, self.urlKey)
        self.asyncQueueLow.enqueue(Click2MySQL, data)

    def register_cep(self):
        return {"after_request_hook": self.Record_ip_pv}

    def register_tep(self):
        """注册博客详情页功能区代码"""
        tep = {"blog_show_funcarea_string": "<scan id='AccessCount'></scan>", "blog_show_script_include": "AccessCountJs.html"}
        return tep

    def register_bep(self):
        """ 注册一个查询uv接口 """
        return {"prefix": "/AccessCount", "blueprint": AccessCountBlueprint}
