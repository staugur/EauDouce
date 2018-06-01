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
import logging

basedir = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO,
                    format='[ %(levelname)s ] %(asctime)s %(filename)s:%(lineno)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=os.path.join(basedir, 'Cleanup.log'),
                    filemode='a')


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


def timestamp_to_timestring(timestamp, format='%Y-%m-%d %H:%M:%S'):
    """ 将时间戳(10位)转换为可读性的时间 """
    # timestamp为传入的值为时间戳(10位整数)，如：1332888820
    timestamp = time.localtime(timestamp)
    # 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    return time.strftime(format, timestamp)


logging.info("Run at {}".format(timestamp_to_timestring(get_current_timestamp())))
for root in os.listdir(basedir):
    root = os.path.join(basedir, root)
    if os.path.isdir(root):
        #判断是否锁目录中
        lock = False
        if os.path.exists(os.path.join(root, "board.lock")):
            lock = True
            logging.info("Locking for {}".format(root))
        for f in os.listdir(root):
            filepath = os.path.join(root, f)
            if ".zip" == os.path.splitext(f)[-1]:
                timestamp = int(os.path.splitext(f)[0].split("_")[-1])
                if timestamp_after_timestamp(timestamp, hours=24) <= get_current_timestamp():
                    logging.info("Remove zip file: {}".format(filepath))
                    os.remove(filepath)
            else:
                if lock is False:
                    logging.info("Remove picture file: {}".format(filepath))
                    os.remove(filepath)
        try:
            os.rmdir(root)
        except OSError:
            pass
