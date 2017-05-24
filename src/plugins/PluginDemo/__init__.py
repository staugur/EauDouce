# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.PluginDemo
    ~~~~~~~~~~~~~~

    This is a demo for plugin.
    You

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

#: Importing these two modules is the first and must be done.
#: 首先导入这两个必须模块
from __future__ import absolute_import
from libs.base import PluginBase
#: Import the other modules here, and if it's your own module, use the relative Import. eg: from .lib import Lib
#: 在这里导入其他模块, 如果有自定义包目录, 使用相对导入, 如: from .lib import Lib


#：Your plug-in name must be consistent with the plug-in directory name.
#：你的插件名称，必须和插件目录名称等保持一致.
__name__        = "PluginDemo"
#: Plugin describes information. What does it do?
#: 插件描述信息,什么用处.
__description__ = "A demo"
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
__readme_file__= "README"


#: 返回插件主类
def getPluginClass():
    return PluginDemoMain

#: 插件主类, 不强制要求名称与插件名一致, 保证getPluginClass准确返回此类
class PluginDemoMain(PluginBase):
    """ 继承自PluginBase基类 """

    def run(self):
        """ 运行插件入口 """
        self.logger.info("I am PluginDemoMain, run!")
