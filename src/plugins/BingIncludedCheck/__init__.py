# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.BingIncludedCheck
    ~~~~~~~~~~~~~~

    Check if Baidu has included a URL plugin.

    :copyright: (c) 2018 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from libs.base import PluginBase
from config import PLUGINS

__name__        = "BingIncludedCheck"
__description__ = "检查必应是否收录博客文章的插件"
__author__      = "Mr.tao <staugur@saintic.com>"
__version__     = "0.1" 
if PLUGINS["BingIncludedCheck"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"

def getPluginClass():
    return BingIncludedCheckMain

class BingIncludedCheckMain(PluginBase):

    def register_tep(self):
        return {"blog_show_funcarea_string": "<scan id='BingIncludedCheck'></scan>", "blog_show_script_include": "BingCheckJs.html"}
