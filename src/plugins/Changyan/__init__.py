# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.Changyan
    ~~~~~~~~~~~~~~

    A Comment System

    :copyright: (c) 2018 by Mr.tao.
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
__name__        = "Changyan"
#: Plugin describes information. What does it do?
#: 插件描述信息,什么用处.
__description__ = "畅言评论系统"
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
if PLUGINS["ChangyanComment"]["enable"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"


#: 返回插件主类
def getPluginClass():
    return ChangyanComment

#: 插件主类, 不强制要求名称与插件名一致, 保证getPluginClass准确返回此类
class ChangyanComment(PluginBase):
    """ 继承自PluginBase基类 """

    def register_tep(self):
        """注册模板入口, 返回扩展点名称及扩展的代码, 其中include点必须是实际的HTML文件, string点必须是HTML代码."""
        return {"blog_index_infolist": "Changyan/index_infolist.html", "blog_show_funcarea": "Changyan/blog_func.html", "blog_show_content": "Changyan/blog_content.html", "blog_show_script": "Changyan/blog_script.html"}
