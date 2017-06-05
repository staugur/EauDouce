# -*- coding: utf-8 -*-
"""
    EauDouce.utils.qf
    ~~~~~~~~~~~~~~

    Queue function.

    :copyright: (c) 2017 by Mr.tao.
    :license: Apache2.0, see LICENSE for more details.
"""

from utils.tool import logger
from libs.base import ServiceBase

_sb = ServiceBase()


def Click2MySQL(data):
    if isinstance(data, dict):
        if data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
            sql = "insert into blog_clicklog set url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s"
            try:
                _sb.mysql_write.insert(sql, data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"))
            except Exception, e:
                logger.warn(e, exc_info=True)


def Click2Redis(data, pvKey, ipKey, urlKey):
    """ 记录ip、ip """

    if isinstance(data, dict):
        try:
            pipe  = _sb.redis.pipeline()
            pipe.incr(pvKey)
            pipe.sadd(ipKey, data.get("ip"))
            key   = data.get("url")
            value = int(pipe.hgetall(urlKey).get(key) or 0)
            value += 1
            pipe.hset(urlKey, key, value)
            pipe.execute()
        except Exception,e:
            logger.error(e, exc_info=True)
        else:
            return True
