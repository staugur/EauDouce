# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.BaiduStatistics
    ~~~~~~~~~~~~~~

    Access statistics using third party Baidu statistical services statistics.
    http://tongji.baidu.com/web/22558594/overview/index?siteId=10025068&castk=30170hd7a5ea318a1d337

    :copyright: (c) 2017 by Mr.tao.
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
__plugin_name__ = "BaiduStatistics"
#: Plugin describes information. What does it do?
#: 插件描述信息,什么用处.
__description__ = "百度统计插件"
#: Plugin Author
#: 插件作者
__author__      = "Mr.tao <staugur@saintic.com>"
#: Plugin Version
#: 插件版本
__version__     = "0.1" 
#: Plugin Url
#: 插件主页
__url__         = "https://www.saintic.com"
#: Plugin License
#: 插件许可证
__license__     = "MIT"
#: Plugin License File
#: 插件许可证文件
__license_file__= "LICENSE"
#: Plugin Readme File
#: 插件自述文件
__readme_file__ = "README"
#: 插件状态, enabled、disabled, 默认enabled
if PLUGINS["BaiduStatistics"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"

#: 返回插件主类
def getPluginClass():
    return BaiduStatisticsPlugin

class BaiduStatisticsPlugin(PluginBase):
    
    __doc__ = __description__

    def register_tep(self):
        return {"base_front_script": "BaiduStatistics/BaiduStatistics.html"}
