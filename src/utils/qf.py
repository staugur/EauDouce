# -*- coding: utf-8 -*-
"""
    EauDouce.utils.qf
    ~~~~~~~~~~~~~~

    Queue function.

    :copyright: (c) 2017 by Mr.tao.
    :license: Apache2.0, see LICENSE for more details.
"""

from .tool import logger
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

    logger.debug('start click2redis')
    if isinstance(data, dict):
        try:
            _sb.redis.incr(pvKey)
            _sb.redis.sadd(ipKey, data.get("ip"))
            key   = data.get("url")
            value = _sb.redis.hgetall(urlKey).get(key)
            if value:
                try:
                    value = int(value) + 1
                except:
                    value = 1
            else:
                value = 1
            logger.debug("click2redis uv key:{0}, value:{1}".format(key, value))
            _sb.redis.hset(urlKey, key, value)
        except Exception,e:
            logger.error(e, exc_info=True)
        else:
            logger.info("Click2Redis uv result {0}:{1}".format(key, value))
