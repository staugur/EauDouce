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
from flask import Blueprint, jsonify, request, g

__plugin_name__ = "AccessCount"
__description__ = "IP、PV、UV统计插件"
__author__      = "Mr.tao"
__version__     = "0.2.0"
__license__     = "MIT"
if PLUGINS["AccessCount"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"


pb = PluginBase()
blogPvKey = "EauDouce:AccessCount:pv:blogs"
AccessCountBlueprint = Blueprint("AccessCount", "AccessCount")
@AccessCountBlueprint.route("/uv/")
def uv():
    url = request.args.get("url")
    res = {"code": 0, "msg": None, "data": None, "url": url}
    if url:
        uri = url.split("/")[-1]
        res.update(data=pb.redis.hget(blogPvKey, uri) or 0)
    return jsonify(res)

def getPluginClass():
    return AccessCount

class AccessCount(PluginBase):
    """记录与统计每天访问数据"""

    def Record_ip_pv(self, *args, **kwargs):
        """ 记录ip、ip """
        resp = kwargs.get("response") or args[0]
        pvKey = "EauDouce:AccessCount:pv:hash"
        pipe = pb.redis.pipeline()
        if request.endpoint in ("front.blogShow", "front.blogEnjoy") and resp.status_code == 200:
            pipe.hincrby(blogPvKey, request.path.split("/")[-1], 1)
        if request.endpoint == "api.wechatapplet" and request.args.get("Action") == "get_blogId":
            pipe.hincrby(blogPvKey, "%s.html" % request.args.get("blogId"), 1)
        # pv
        pipe.hincrby(pvKey, get_today("%Y%m%d"), 1)
        try:
            pipe.execute()
        except:
            pass

    def register_hep(self):
        return {"after_request_hook": self.Record_ip_pv}

    def register_tep(self):
        """注册博客详情页功能区代码"""
        tep = {"blog_show_funcarea": "<scan id='AccessCount'></scan>", "blog_show_script": "AccessCountJs.html"}
        return tep

    def register_bep(self):
        """ 注册一个查询uv接口 """
        return {"prefix": "/AccessCount", "blueprint": AccessCountBlueprint}
