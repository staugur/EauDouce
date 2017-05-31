# -*- coding: utf-8 -*-
"""
    EauDouce.rq_worker
    ~~~~~~~~~~~~~~

    The working process of the RQ queue.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from config import GLOBAL, REDIS
from utils.tool import logger
from redis import from_url
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']
ProcessName = "{0}{1}".format(GLOBAL.get('ProcessName'), ".RQ")

try:
    import setproctitle
except ImportError, e:
    logger.warn("%s, try to pip install setproctitle, otherwise, you can't use the process to customize the function" %e)
else:
    setproctitle.setproctitle(ProcessName)
    logger.info("The process is %s" % ProcessName)

if __name__ == '__main__':
    with Connection(from_url(REDIS)):
        worker = Worker(map(Queue, listen))
        worker.work()
