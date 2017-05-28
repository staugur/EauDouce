# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.BaiduIncludedCheck
    ~~~~~~~~~~~~~~

    Check if Baidu has included a URL plugin.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from libs.base import PluginBase
from flask import Blueprint, jsonify, request
from .util import BaiduIncludedCheckUtil

__name__        = "BaiduIncludedCheck"
__description__ = "检查百度是否收录某URL的插件"
__author__      = "Mr.tao <staugur@saintic.com>"
__version__     = "0.1" 
__state__       = "enabled"

tool = BaiduIncludedCheckUtil()
BaiduIncludedCheckBlueprint = Blueprint("BaiduIncludedCheck", "BaiduIncludedCheck")
@BaiduIncludedCheckBlueprint.route("/")
def index():
    url = request.args.get("url")
    res = {"code": 0, "msg": None, "Included": False, "url": url}
    if url:
        Included = True if tool.check(url) else False
        res.update(Included=Included)
    else:
        res.update(msg="Request parameter error: no url")
    return jsonify(res)

def getPluginClass():
    return BaiduIncludedCheck

class BaiduIncludedCheck(PluginBase):

    def register_bep(self):
        return {"prefix": "/BaiduIncludedCheck", "blueprint": BaiduIncludedCheckBlueprint}
        