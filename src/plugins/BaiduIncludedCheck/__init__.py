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
from config import PLUGINS

__plugin_name__ = "BaiduIncludedCheck"
__description__ = "检查百度是否收录某URL的插件"
__author__      = "Mr.tao <staugur@saintic.com>"
__version__     = "0.1" 
if PLUGINS["BaiduIncludedCheck"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"

def getPluginClass():
    return BaiduIncludedCheck

class BaiduIncludedCheck(PluginBase):

    def register_tep(self):
        return {"blog_show_funcarea": "<scan id='BaiduIncludedCheck'></scan>", "blog_show_script": "BaiduCheckJs.html"}
