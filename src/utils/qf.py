# -*- coding: utf-8 -*-
"""
    EauDouce.utils.qf
    ~~~~~~~~~~~~~~

    Queue function.

    :copyright: (c) 2017 by Mr.tao.
    :license: Apache2.0, see LICENSE for more details.
"""
import os, sys, time, shutil, requests
from .tool import logger, getIpArea, get_current_timestamp, get_today
from libs.base import ServiceBase
from user_agents import parse as user_agents_parse
from multiprocessing.dummy import Pool as ThreadPool
reload(sys)
sys.setdefaultencoding('utf-8')

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


def DownloadBoard(basedir, board_id, zipfilename, board_pins):
    """
    @param basedir str: 画板上层目录，CrawlHuaban插件所在目录，图片直接保存到此目录的`board_id`下
    @param board_id str int: 画板id
    @param zipfilename str: 压缩文件名称
    @param board_pins list: pin图片列表
    """
    logger.sys.debug("DownloadBoard dir: {}, board_pins number: {}".format(basedir, len(board_pins)))
    req = requests.Session()
    req.headers.update({'Referer': 'http://huaban.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'})
    def makedir(d):
        d = str(d)
        if not os.path.exists(d):
            os.makedirs(d)
        if os.path.exists(d):
            return True
        else:
            return False
    def _download_img(pin, retry=True):
        """ 下载单个图片
        @param pin dict: pin的数据，要求： {'imgUrl': xx, 'imgName': xx}
        @param retry bool: 是否失败重试
        """
        if pin and isinstance(pin, dict) and "imgUrl" in pin and "imgName" in pin:
            imgurl = pin['imgUrl']
            imgname = os.path.join(basedir, board_id, pin['imgName'])
            logger.sys.debug(imgname)
            if not os.path.isfile(imgname):
                try:
                    res = req.get(imgurl)
                    with open(imgname, 'wb') as fp:
                        fp.write(res.content)
                except Exception,e:
                    if retry is True:
                        _download_img(pin, False)
    os.chdir(basedir)
    makedir(board_id)
    pool = ThreadPool()
    data = pool.map(_download_img, board_pins)
    pool.close()
    pool.join()
    logger.sys.debug("DownloadBoard over, data len: {}, start make_archive".format(len(data)))
    zipfilepath = shutil.make_archive(zipfilename, 'zip', board_id)
    logger.sys.debug("DownloadBoard make_archive over, path is {}".format(zipfilepath))
    zipfilename = "{}.zip".format(zipfilename)
    shutil.move(zipfilename, os.path.join(board_id, zipfilename))
