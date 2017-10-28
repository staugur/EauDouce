# -*- coding: utf-8 -*-
"""
    EauDouce.utils.qf
    ~~~~~~~~~~~~~~

    Queue function.

    :copyright: (c) 2017 by Mr.tao.
    :license: Apache2.0, see LICENSE for more details.
"""

from .tool import logger, getIpArea
from libs.base import ServiceBase
from user_agents import parse as user_agents_parse

_sb = ServiceBase()

def Click2MySQL(data):
    url = data.get("url")
    logger.access.info("url: {}, rq in: {}, static in: {}".format(url, not "/rqdashboard" in url, not "/static" in url))
    if isinstance(data, dict) and not "/rqdashboard" in data.get("url") and not "/static/" in data.get("url"):
        if data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
            # 解析User-Agent
            uap = user_agents_parse(data.get("agent"))
            browserDevice, browserOs, browserFamily = str(uap).split(' / ')
            if uap.is_mobile:
                browserType = "mobile"
            elif uap.is_pc:
                browserType = "pc"
            elif uap.is_tablet:
                browserType = "tablet"
            elif uap.is_bot:
                browserType = "bot"
            else:
                browserType = "unknown"
            sql = "insert into blog_clicklog set url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s, isp=%s, browserType=%s, browserDevice=%s, browserOs=%s, browserFamily=%s"
            try:
                _sb.mysql_write.insert(sql, data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"), getIpArea(data.get("ip")), browserType, browserDevice, browserOs, browserFamily)
            except Exception, e:
                logger.plugin.warn(e, exc_info=True)


def Click2Redis(data, pvKey, ipKey, urlKey):
    """ 记录ip、ip """

    logger.sys.debug('start click2redis')
    if isinstance(data, dict):
        try:
            pipe = _sb.redis.pipeline()
            #_sb.redis.incr(pvKey)
            #_sb.redis.sadd(ipKey, data.get("ip"))
            pipe.incr(pvKey)
            pipe.sadd(ipKey, data.get("ip"))
            key   = data.get("url")
            value = _sb.redis.hgetall(urlKey).get(key)
            try:
                value = int(value)
            except Exception:
                value = 1
            value += 1
            pipe.hset(urlKey, key, value)
            pipe.execute()
        except Exception,e:
            logger.sys.error(e, exc_info=True)
        else:
            logger.sys.info("Click2Redis uv result {0}:{1}".format(key, value))
