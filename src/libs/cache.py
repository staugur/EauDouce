# -*- coding: utf8 -*-
# Cache blog data

from flask.ext.cache import Cache
from config import REDIS, PLUGINS
from utils.tool import logger, ParseRedis

_info = ParseRedis(REDIS) or {}

config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': _info.get("host", "127.0.0.1"),
    'CACHE_REDIS_PORT': _info.get("port", 6379),
    'CACHE_REDIS_DB': _info.get("db", 0),
    'CACHE_REDIS_PASSWORD': _info.get("password", None)
} if PLUGINS['Cache'] == 'redis' else {
    'CACHE_TYPE': 'simple'
}

logger.info("cache config is {}".format(config))
cache = Cache(config=config)