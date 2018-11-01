# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.BaiduActivePush
    ~~~~~~~~~~~~~~

    百度主动推送(实时)插件

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from libs.base import PluginBase
from config import PLUGINS

__plugin_name__ = "BaiduActivePush"
__description__ = "百度主动推送(实时)插件"
__author__      = "Mr.tao <staugur@saintic.com>"
__version__     = "0.1"
if PLUGINS["BaiduActivePush"]["enable"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"

def getPluginClass():
    return BaiduActivePushMain

class BaiduActivePushMain(PluginBase):

    def register_tep(self):
        return {"blog_show_funcarea": "<scan id='BaiduActivePush'></scan>", "blog_show_script": "BaiduActivePush.html"}