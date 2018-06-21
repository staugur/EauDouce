# -*- coding: utf-8 -*-
"""
    EauDouce.utils.qf
    ~~~~~~~~~~~~~~

    Queue function.

    :copyright: (c) 2017 by Mr.tao.
    :license: Apache2.0, see LICENSE for more details.
"""
import os, sys, time, shutil, requests
from .tool import logger, getIpArea, get_current_timestamp, get_today, make_zipfile
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


def DownloadBoard(basedir, board_id, zipfilename, board_pins, ctime, etime):
    """
    @param basedir str: 画板上层目录，CrawlHuaban插件所在目录，图片直接保存到此目录的`board_id`下
    @param board_id str int: 画板id
    @param zipfilename str: 压缩文件名称
    @param board_pins list: pin图片列表
    @param ctime, etime int: 分别是创建时间和过期时间，仅用于写入mysql
    """
    logger.sys.debug("DownloadBoard dir: {}, board_pins number: {}".format(basedir, len(board_pins)))
    #初始写入数据库
    try:
        _sb.mysql_write.insert("insert into plugin_crawlhuaban (board_id,filename,pin_number,ctime,etime) values(%s,%s,%s,%s,%s)", board_id, zipfilename, len(board_pins), ctime, etime)
    except Exception,e:
        logger.sys.error(e, exc_info=True)
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
    lock_file = os.path.join(board_id, "board.lock")
    with open(lock_file, 'w') as f:
        f.write("")
    pool = ThreadPool()
    data = pool.map(_download_img, board_pins)
    pool.close()
    pool.join()
    logger.sys.debug("DownloadBoard over, data len: {}, start make_archive".format(len(data)))
    zipfilepath = make_zipfile(zipfilename, board_id, [".zip", ".lock"])
    logger.sys.debug("DownloadBoard make_archive over, path is {}".format(zipfilepath))
    shutil.move(zipfilename, os.path.join(board_id, zipfilename))
    os.remove(lock_file)
    logger.sys.debug("DownloadBoard move over, delete lock")
    try:
        _sb.mysql_write.update("update plugin_crawlhuaban set status=1 where board_id=%s and filename=%s", board_id, zipfilename)
    except Exception,e:
        logger.sys.error(e, exc_info=True)

def DownloadBoardAddTimes(board_id, zipfilename, mtime):
    """更新下载画板压缩包次数
    @param board_id str int: 画板id
    @param zipfilename str: 压缩文件名称
    @param mtime str: 更新时间
    """
    sql = "update plugin_crawlhuaban set downloadTimes=downloadTimes + 1,mtime=%s where board_id=%s and filename=%s"
    if board_id and zipfilename and mtime:
        _sb.mysql_write.update(sql, mtime, board_id, zipfilename)
