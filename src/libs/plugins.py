# -*- coding: utf-8 -*-
"""
    EauDouce.libs.plugins
    ~~~~~~~~~~~~~~

    Plugins Manager: load and run plugins.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import os
from utils.tool import plugin_logger

class PluginManager(object):
    """
    定义插件基类, 遵循格式如下:
    插件为目录, 目录名称为插件名称, 插件入口文件是__init__.py, 文件内包含name、description、version、author、license、url、README等插件信息.
    静态资源请通过提供的接口上传至又拍云.
    plugins/
    ├── plugin1
    │   ├── __init__.py
    │   ├── LICENSE
    │   ├── README
    │   └── templates
    │       └── plugin1
    └── plugin2
        ├── __init__.py
        ├── LICENSE
        ├── README
        └── templates
            └── plugin2
    """

    def __init__(self):
        self.plugins     = []
        self.plugin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugins")
        self.__scanPlugins()

    def __getPluginInfo(self, package, plugin):
        """ 组织插件信息 """
        try:
            url = plugin.__url__
        except AttributeError:
            url = None

        try:
            license = plugin.__license__
        except AttributeError:
            license = None

        try:
            license_file = plugin.__license_file__
        except AttributeError:
            license_file = None

        try:
            readme_file = plugin.__readme_file__
        except AttributeError:
            readme_file = None

        return {
            "plugin_name": plugin.__name__,
            "plugin_description": plugin.__description__,
            "plugin_version": plugin.__version__,
            "plugin_author": plugin.__author__,
            "plugin_url": url,
            "plugin_license": license,
            "plugin_license_file": license_file,
            "plugin_readme_file": readme_file,
            "plugin_state": "enabled",
            "plugin_tpl_path": os.path.join("plugins", package, "templates", package)
        }

    def __scanPlugins(self):
        """ 扫描插件目录 """
        plugin_logger.info("Initialization Plugins Start, loadPlugins path: {0}".format(self.plugin_path))
        if os.path.exists(self.plugin_path):
            for package in os.listdir(self.plugin_path):
                _plugin_path = os.path.join(self.plugin_path, package)
                if os.path.isdir(_plugin_path):
                    if os.path.isfile(os.path.join(_plugin_path, "__init__.py")):
                        plugin_logger.info("find plugin package: {0}".format(package))
                        self.__runPlugins(package)
        else:
            plugin_logger.warning("Plugins directory not in here!")

    def __runPlugins(self, package):
        """ 动态加载插件模块,遵循插件格式的才能被启用并运行,否则删除加载 """

        #: 动态加载模块(plugins.package): 可以查询自定义的信息, 并通过getPluginClass获取插件的类定义
        plugin = __import__("{0}.{1}".format("plugins", package), fromlist=["plugins",])
        #: 检测插件信息
        if plugin.__name__ and plugin.__version__ and plugin.__description__ and plugin.__author__:
            #: 获取插件信息
            pluginInfo = self.__getPluginInfo(package, plugin)
            #: 获取插件主类并实例化
            p = plugin.getPluginClass()
            i = p()
            plugin_logger.info("runPlugin: package is {0}.{1}, class instance is {2}".format("plugins", package, i))
            #: 更新插件信息
            pluginInfo.update(plugin_instance=i)
            #: 运行插件主类的run方法
            if hasattr(i, "run"):
                i.run()
                self.plugins.append(pluginInfo)
            else:
                plugin_logger.error("The current class {0} does not have the `run` method".format(i))
        else:
            del plugin
            plugin_logger.warning("This plugin `{0}` is not enabled without following the standard plugin format".format(package))

    @property
    def get_all_plugins(self):
        return self.plugins
