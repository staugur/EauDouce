# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.CrawlHuaban.Cleanup
    ~~~~~~~~~~~~~~

    定时清理抓取花瓣网画板的图片

    :copyright: (c) 2018 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

import os
import time
import datetime

basedir = os.path.dirname(os.path.abspath(__file__))


def get_current_timestamp():
    """ 获取本地当前时间戳(10位): Unix timestamp：是从1970年1月1日（UTC/GMT的午夜）开始所经过的秒数，不考虑闰秒 """
    return int(time.mktime(datetime.datetime.now().timetuple()))


def timestamp_after_timestamp(timestamp=None, seconds=0, minutes=0, hours=0, days=0):
    """ 给定时间戳(10位),计算该时间戳之后多少秒、分钟、小时、天的时间戳(本地时间) """
    # 1. 默认时间戳为当前时间
    timestamp = get_current_timestamp() if timestamp is None else timestamp
    # 2. 先转换为datetime
    d1 = datetime.datetime.fromtimestamp(timestamp)
    # 3. 根据相关时间得到datetime对象并相加给定时间戳的时间
    d2 = d1 + datetime.timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    # 4. 返回某时间后的时间戳
    return int(time.mktime(d2.timetuple()))


for root, dirs, files in os.walk(basedir):
    if os.path.isdir(root):
        for f in files:
            path = os.path.join(basedir, root, f)
            if ".zip" == os.path.splitext(f)[-1]:
                timestamp = os.path.splitext(f)[0].split("_")[-1]
                if timestamp_after_timestamp(int(timestamp), hours=24) <= get_current_timestamp():
                    print "remove {}".format(path)
                    os.remove(path)
            else:
                os.remove(path)
