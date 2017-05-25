# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.Reward
    ~~~~~~~~~~~~~~

    仿百度打赏的博客打赏组件,给博客添加模仿百度打赏的打赏组件,基于张戈博客代码略微修改适应JQuery3.0+

    :copyright: (c) 2017 by Ivan Sagalaev.
    :license: BSD-3-Clause, see LICENSE for more details.
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
__name__        = "Reward"
#: Plugin describes information. What does it do?
#: 插件描述信息,什么用处.
__description__ = "Add a reward component to a blog that mimics Baidu's reward"
#: Plugin Author
#: 插件作者
__author__      = "zhangge.net"
#: Plugin Version
#: 插件版本
__version__     = "0.1" 
#: Plugin Url
#: 插件主页
__url__         = "http://zhangge.net/5110.html"
#: Plugin License
#: 插件许可证
__license__     = "MIT"
#: 插件状态, enabled、disabled, 默认enabled
if PLUGINS["Reward"] in ("true", "True", True):
    __state__       = "enabled"
else:
    __state__       = "disabled"

#: 返回插件主类
def getPluginClass():
    return Reward

class Reward(PluginBase):
    
    __doc__ = __description__

    def register_tep(self):
        return {"blog_show_content_include": "Reward/Reward.html", "blog_show_script_include": "Reward/RewardJs.html"}
