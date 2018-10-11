# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.BaiduShare
    ~~~~~~~~~~~~~~

    Baidu social sharing service

    :copyright: (c) 2017 by Ivan Sagalaev.
    :license: MIT, see LICENSE for more details.
"""

#: Importing these two modules is the first and must be done.
#: 首先导入这两个必须模块
from __future__ import absolute_import
from libs.base import PluginBase
#: Import the other modules here, and if it's your own module, use the relative Import. eg: from .lib import Lib
#: 在这里导入其他模块, 如果有自定义包目录, 使用相对导入, 如: from .lib import Lib
from config import PLUGINS

#：Your plug-in name must be consistent with the plug-in directory name.
#：你的插件名称，必须和插件目录名称等保持一致.
__name__        = "shareJs"
#: Plugin describes information. What does it do?
#: 插件描述信息,什么用处.
__description__ = "一键分享到微博、QQ空间、QQ好友、微信、腾讯微博、豆瓣、Facebook、Twitter、Linkedin、Google+、点点等"
#: Plugin Author
#: 插件作者
__author__      = "overtrue"
#: Plugin Version
#: 插件版本
__version__     = "1.0.2" 
#: Plugin Url
#: 插件主页
__url__         = "https://github.com/overtrue/share.js"
#: Plugin License
#: 插件许可证
__license__     = "MIT"
#: 插件状态, enabled、disabled, 默认enabled
if PLUGINS["shareJs"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"

#: 返回插件主类
def getPluginClass():
    return shareJs

class shareJs(PluginBase):
    
    __doc__ = __description__

    def register_tep(self):
        return {"blog_show_header": '<link rel="stylesheet" href="/static/share.js/css/share.min.css">', "blog_show_content": "1@shareJs.html"}
