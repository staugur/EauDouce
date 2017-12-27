# -*- coding: utf-8 -*-
"""
    EauDouce.utils.qf
    ~~~~~~~~~~~~~~

    Queue function.

    :copyright: (c) 2017 by Mr.tao.
    :license: Apache2.0, see LICENSE for more details.
"""

from .tool import logger, getIpArea, get_current_timestamp, get_today
from libs.base import ServiceBase
from user_agents import parse as user_agents_parse

_sb = ServiceBase()

def Click2MySQL(data):
    if isinstance(data, dict):
        if "/rqdashboard" in data.get("url") or "/static/" in data.get("url"):
            return
        if data.get("agent"):
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
            sql = "insert into blog_clicklog set url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s, isp=%s, browserType=%s, browserDevice=%s, browserOs=%s, browserFamily=%s, clickTime=%s"
            try:
                mid = _sb.mysql_write.insert(sql, data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"), getIpArea(data.get("ip")), browserType, browserDevice, browserOs, browserFamily, get_current_timestamp())
            except Exception, e:
                logger.plugin.warn(e, exc_info=True)
            else:
                logger.plugin.debug("Click2MySQL for {}".format(mid))


def Click2Redis(data, pvKey, ipKey, urlKey):
    """ 记录ip、ip """

    if isinstance(data, dict):
        try:
            key  = data.get("url")
            value= _sb.redis.hget(urlKey, key)
            try:
                value = int(value)
            except Exception:
                value = 1
            else:
                value += 1
            pipe = _sb.redis.pipeline()
            pipe.hincrby(pvKey, get_today("%Y%m%d"), 1)
            pipe.sadd(ipKey, data.get("ip"))
            pipe.hset(urlKey, key, value)
            pipe.execute()
        except Exception,e:
            logger.plugin.error(e, exc_info=True)
        else:
            logger.plugin.info("Click2Redis uv result {0}:{1}".format(key, value))
