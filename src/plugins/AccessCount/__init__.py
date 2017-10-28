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
from flask import Blueprint, jsonify, request
from user_agents import parse as user_agents_parse

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
uvKey = "EauDouce:AccessCount:uv"
AccessCountBlueprint = Blueprint("AccessCount", "AccessCount")
@AccessCountBlueprint.route("/uv/")
def uv():
    url = request.args.get("url")
    res = {"code": 0, "msg": None, "data": None, "url": url}
    sql = "select id,url,ip from blog_clicklog where url=%s"
    num = len(pb.mysql_read.query(sql, url))
    res.update(data=num)
    pb.logger.info(res)
    return jsonify(res)

def getPluginClass():
    return AccessCount

class AccessCount(PluginBase):
    """ 记录与统计每天访问数据 """

    def Click2MySQL(self, data):
        if isinstance(data, dict):
            if data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
                # 解析User-Agent
                uap = user_agents_parse(data.get("agent"))
                browserDevice, browserOs, browserFamily = str(uap).split(' / ')
                if uap.is_mobile:
                    browserType = "mobile"
                elif uap.is_pc:
                    browserType = "pc"
                elif uap.is_tablet:
                    browserType = "tablet"
                elif uap.is_bot:
                    browserType = "bot"
                else:
                    browserType = "unknown"
                sql = "insert into blog_clicklog set url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s, browserType=%s, browserDevice=%s, browserOs=%s, browserFamily=%s"
                try:
                    pb.mysql_write.insert(sql, data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"), browserType, browserDevice, browserOs, browserFamily)
                except Exception, e:
                    self.logger.warn(e, exc_info=True)

    def Record_ip_pv(self, **kwargs):
        """ 记录ip、ip """
        data  = kwargs.get("access_data")
        self.Click2MySQL(data)

    def register_cep(self):
        return {"after_request_hook": self.Record_ip_pv}

    def register_tep(self):
        """注册博客详情页功能区代码"""
        tep = {"blog_show_funcarea_string": "<scan id='AccessCount'></scan>", "blog_show_script_include": "AccessCountJs.html"}
        return tep

    def register_bep(self):
        """ 注册一个查询uv接口 """
        return {"prefix": "/AccessCount", "blueprint": AccessCountBlueprint}
