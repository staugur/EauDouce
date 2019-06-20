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
blogPvKey = "EauDouce:AccessCount:pv:blogs"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--migrate_pv_from_mysql_to_redis", default=False, action='store_true')
    parser.add_argument("--refresh_blog_pv", help=u"将博客文章的pv刷入mysql中", default=False, action='store_true')
    args = parser.parse_args()
    migrate_pv_from_mysql_to_redis = args.migrate_pv_from_mysql_to_redis
    refresh_blog_pv = args.refresh_blog_pv
    if migrate_pv_from_mysql_to_redis:
        blog_ids = [ i["id"] for i in sb.mysql_read.query("select id from blog_article") ]
        failed = []
        for bid in range(85,273):
            if bid not in blog_ids:
                continue
            sql = "SELECT count(id) as count FROM blog_clicklog WHERE url LIKE '%%{}.html%%'".format(bid)
            try:
                data = sb.mysql_write.get(sql)
            except:
                failed.append(bid)
            else:
                pv = data.get("count")
                sb.redis.hset(blogPvKey, "{}.html".format(bid), pv)
        print failed
    if refresh_blog_pv:
        sql = "update blog_article set pv=%s where id=%s"
        data = sb.redis.hgetall(blogPvKey)
        for path,pv in data.iteritems():
            bid = path.split('.')[0]
            try:
                sb.mysql_write.update(sql, pv, bid)
            except:
                pass
    if not migrate_pv_from_mysql_to_redis and not refresh_blog_pv:
        parser.print_help()
