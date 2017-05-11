#!/usr/bin/python -O
# -*- coding: utf8 -*-
#product environment start application with `gevent server`
#pip install gevent

from main import app
from config import GLOBAL
from utils.tool import logger

Host = "0.0.0.0"
Port = GLOBAL.get('Port')
Environment = GLOBAL.get('Environment')
ProcessName = GLOBAL.get('ProcessName')

try:
    import setproctitle
except ImportError, e:
    logger.warn("%s, try to pip install setproctitle, otherwise, you can't use the process to customize the function" %e)
else:
    setproctitle.setproctitle(ProcessName)
    logger.info("The process is %s" % ProcessName)

try:
    msg = '%s has been launched, %s:%s' %(ProcessName, Host, Port)
    print(msg)
    logger.info(msg)

    from gevent.wsgi import WSGIServer
    http_server = WSGIServer((Host, Port), app)
    http_server.serve_forever()

except Exception,e:
    print(e)
    logger.error(e, exc_info=True)
