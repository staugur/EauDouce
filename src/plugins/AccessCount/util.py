# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.AccessCount.util
    ~~~~~~~~~~~~~~

    AccessCount util.

    :copyright: (c) 2017 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

from utils.tool import logger

def Click2MySQL(mysql, data):
    if isinstance(data, dict):
        if data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
            sql = "insert into clickLog set requestId=%s, url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s"
            try:
                mysql.insert(sql, data.get("requestId"), data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"))
            except Exception, e:
                logger.warn(e, exc_info=True)


def Click2Redis(redis, data, pvKey, ipKey):
    """ 记录ip、ip """

    if isinstance(data, dict):
        try:
            redis.incr(pvKey)
            redis.sadd(ipKey, data.get("ip"))
        except Exception,e:
            logger.error(e, exc_info=True)
        else:
            return True
