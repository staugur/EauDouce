#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
    EauDouce.cli
    ~~~~~~~~~~~~~~

    Cli Entrance

    :copyright: (c) 2018 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import os
import json
from libs.base import ServiceBase
from utils.tool import logger, get_current_timestamp, timestamp_after_timestamp

_sb = ServiceBase()
basedir = os.path.dirname(os.path.abspath(__file__))


def execute_cleanCrawlHuaban():
    """执行清理花瓣网插件目录下过期的压缩文件"""
    huabandir = os.path.join(basedir, "plugins", "CrawlHuaban")
    for root in os.listdir(huabandir):
        board_id, root = root, os.path.join(huabandir, root)
        if os.path.isdir(root):
            # 判断是否锁目录中
            lock = False
            if os.path.exists(os.path.join(root, "board.lock")):
                lock = True
                logger.cli.info("Locking for {}".format(root))
            for f in os.listdir(root):
                filepath = os.path.join(root, f)
                if ".zip" == os.path.splitext(f)[-1]:
                    timestamp = int(os.path.splitext(f)[0].split("_")[-1])
                    if timestamp_after_timestamp(timestamp, hours=24) <= get_current_timestamp():
                        logger.cli.info("Remove zip file: {}".format(filepath))
                        try:
                            os.remove(filepath)
                            _sb.mysql_write.update("update plugin_crawlhuaban set status=2,mtime=%s where board_id=%s and filename=%s", get_current_timestamp(), board_id, f)
                        except Exception,e:
                            logger.cli.error(e, exc_info=True)
                else:
                    if lock is False:
                        os.remove(filepath)
            try:
                os.rmdir(root)
            except OSError:
                pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleanCrawlHuaban", help=u"清理抓取花瓣网插件的过期目录及压缩文件", default=False, action='store_true')
    args = parser.parse_args()
    cleanCrawlHuaban = args.cleanCrawlHuaban
    if cleanCrawlHuaban:
        execute_cleanCrawlHuaban()
    else:
        parser.print_help()
