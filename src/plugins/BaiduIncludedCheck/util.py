# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.BaiduIncludedCheck.util
    ~~~~~~~~~~~~~~

    util tool.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from libs.base import PluginBase
from bs4 import BeautifulSoup
import requests


class BaiduIncludedCheckUtil(PluginBase):
    """ 百度收录查询 """

    QueueKey = "EauDouce_BaiduIncludedCheck_Sq"

    def _put(self, value):
        """ 向队列写数据 """
        return self.redis.rpush(self.QueueKey, value)

    def _get(self, value):
        """ 查询value是否在队列中 """
        #_queue_length = self.redis.llen(self.QueueKey)
        _queue_data   = self.redis.lrange(self.QueueKey, 0, -1)
        return True if value in _queue_data else False

    def check(self, url):
        """ 百度收录查询入口 """
        if self._get(url):
            return True
        else:
            # 设置UA模拟用户，还可设置多个UA提高搜索成功率
            headers = {'User-Agent': 'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)'}
            # 构建百度搜索URL；因为是查收录，所以只显示了前1个搜索结果，还可以通过rn参数来调整搜索结果的数量，不过结果数量越多，速度越慢，因为每个结果都要请求下获取真实URL。
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
                    # 待查URL匹配百度搜索结果的真实URL，如果匹配就表示收录，循环完毕仍未匹配则未收录, 返回False
                    curl = url.split("://")[-1] if "://" in url else url
                    if r.url.split("://")[-1] == curl:
                        self._put(url)
                        return True
            return False