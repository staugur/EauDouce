#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    EauDouce.cli
    ~~~~~~~~~~~~

    Cli Entrance


    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from libs.base import ServiceBase
sb = ServiceBase()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh_blog_pv", help=u"将博客文章的pv刷入mysql中", default=False, action='store_true')
    args = parser.parse_args()
    refresh_blog_pv = args.refresh_blog_pv
    if refresh_blog_pv:
        blogPvKey = "EauDouce:AccessCount:pv:blogs"
        sql = "update blog_article set pv=%s where id=%s"
        data = sb.redis.hgetall(blogPvKey)
        for path,pv in data.iteritems():
            bid = path.split('.')[0]
            try:
                sb.mysql_write.update(sql, pv, bid)
            except:
                pass
    if not refresh_blog_pv:
        parser.print_help()
