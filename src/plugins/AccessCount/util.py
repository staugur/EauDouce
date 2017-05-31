# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.AccessCount.util
    ~~~~~~~~~~~~~~

    AccessCount util.

    :copyright: (c) 2017 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""
from libs.base import ServiceBase
from utils.tool import logger

sb = ServiceBase()

def Click2MySQL(data):
    if isinstance(data, dict):
        if data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
            sql = "insert into blog_clicklog set url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s"
            try:
                sb.mysql_write.insert(sql, data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"))
            except Exception, e:
                logger.warn(e, exc_info=True)


def Click2Redis(data, pvKey, ipKey):
    """ 记录ip、ip """

    if isinstance(data, dict):
        try:
            sb.redis.incr(pvKey)
            sb.redis.sadd(ipKey, data.get("ip"))
        except Exception,e:
            logger.error(e, exc_info=True)
        else:
            return True
