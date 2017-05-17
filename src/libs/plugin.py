# -*- coding: utf8 -*-
#
# 插件基类
#

class Plugin(object):
    """ 定义一个接口，其他 插件必须实现这个接口，name 属性必须赋值 """
    name = ''
    description = ''
    version = ''
    
    def __init__(self):
        pass
    
    def executeFun(self):
        pass
