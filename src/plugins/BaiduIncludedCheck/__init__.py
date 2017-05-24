# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.BaiduIncludedCheck
    ~~~~~~~~~~~~~~

    Check if Baidu has included a URL plugin.

    :copyright: (c) 2017 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

__name__        = "BaiduIncludedCheck"
__description__ = "Check if Baidu has included a URL plugin."
__author__      = "taochengwei <taochengwei@starokay.com>"
__version__     = "0.1" 

import requests
from bs4 import BeautifulSoup
from libs.base import PluginBase


def getPluginClass():
    return "BaiduIncludedCheckPluginManager"


class BaiduIncludedCheckPluginManager(PluginBase):
    """ Redis简单队列管理器 """

    def __init__(self):
        super(BaiduIncludedCheckPluginManager, self).__init__()
        #定义队列名
        self.QueueKey = "EauDouce_Baidu_Url_Sq"

    def _put(self, value):
        """ 向队列写数据 """
        return self.redis.lrpush(self.QueueKey, value)

    def _get(self, value):
        """ 查询value是否在队列中 """
        _queue_length = self.redis.llen(self.QueueKey)
        _queue_data   = self.redis.lrange(self.QueueKey, 0, _queue_length)
        return True if value in _queue_data else False

    def check(url):
        """ 百度收录查询入口 """
        if self._get(url):
            return True
        else:
            # 设置UA模拟用户，还可设置多个UA提高搜索成功率
            headers = {'User-Agent': 'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)'}
            # 构建百度搜索URL；因为是查收录，所以只显示了前10个搜索结果，还可以通过rn参数来调整搜索结果的数量
            b_url = 'http://www.baidu.com/s?wd=%s&rn=1' % url
            # 初始化BeautifulSoup
            soup = BeautifulSoup(requests.get(b_url, headers=headers, timeout=self.timeout).content, "html.parser")
            # 获取URL的特征值是通过class="t"
            b_links = [tag.a['href'] for tag in soup.find_all('h3', {'class': 't'})]
            # 分析搜索结果中的真实URL,使用requests库获取了最终URL，而不是快照URL
            for link in b_links:
                try:
                    r = requests.get(link, headers=headers, timeout=self.timeout)
                except Exception as e:
                    pass
                else:
                    #待查URL匹配百度搜索结果的真实URL，如果匹配就表示收录，循环完毕仍未匹配则未收录, 返回False
                    curl = url.split("://")[-1] if "://" in url else url
                    if r.url.split("://")[-1] == curl:
                        self._put(url)
                        return True
            return False

    def run(self):
        """ 运行插件入口 """
        self.logger.info("I am BaiduIncludedCheck {0} run!".format(getPluginClass()))