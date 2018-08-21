# -*- coding: utf-8 -*-
"""
    EauDouce.utils.qf
    ~~~~~~~~~~~~~~

    Queue function.

    :copyright: (c) 2017 by Mr.tao.
    :license: Apache2.0, see LICENSE for more details.
"""
import os, sys, time, shutil, requests
from .tool import logger, getIpArea, get_current_timestamp, get_today, make_zipfile, formatSize, email_check
from .send_email_msg import SendMail
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


def DownloadBoard(basedir, board_id, zipfilename, board_pins, total_number, ctime, etime, version, site, user_ip, user_agent, email, downloadUrl):
    """
    @param basedir str: 画板上层目录，CrawlHuaban插件所在目录，图片直接保存到此目录的`board_id`下
    @param board_id str int: 画板id
    @param zipfilename str: 压缩文件名称
    @param board_pins list: pin图片列表
    @param total_number, ctime, etime int: 分别是画板图片总数、创建时间和过期时间，仅用于写入mysql
    @param version, site, user_ip, user_agent str: 分别是用户脚本版本、站点id、用户ip、用户代理，仅用于写入mysql
    """
    logger.sys.debug("DownloadBoard dir: {}, board_pins number: {}".format(basedir, len(board_pins)))
    #初始写入数据库
    try:
        if user_agent:
            # 解析User-Agent
            uap = user_agents_parse(user_agent)
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
        else:
            browserType, browserDevice, browserOs, browserFamily = "", "", "", "", ""
        _sb.mysql_write.insert("insert into plugin_crawlhuaban (site,board_id,filename,pin_number,total_number,ctime,etime,version,user_ip,user_area,user_agent,browser_type,browser_device,browser_os,browser_family) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", site, board_id, zipfilename, len(board_pins), total_number, ctime, etime, version, user_ip, getIpArea(user_ip), user_agent, browserType, browserDevice, browserOs, browserFamily)
    except Exception,e:
        logger.sys.error(e, exc_info=True)
    req = requests.Session()
    req.headers.update({'Referer': 'https://huaban.com/boards/{}'.format(board_id) if site == 1 else 'https://www.duitang.com/album/?id={}'.format(board_id), 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'})
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
    stime = time.time()
    pool = ThreadPool()
    data = pool.map(_download_img, board_pins)
    pool.close()
    pool.join()
    logger.sys.debug("DownloadBoard over, data len: {}, start make_archive".format(len(data)))
    zipfilepath = make_zipfile(zipfilename, board_id, [".zip", ".lock"])
    logger.sys.debug("DownloadBoard make_archive over, path is {}".format(zipfilepath))
    size = formatSize(os.path.getsize(zipfilename))
    shutil.move(zipfilename, os.path.join(board_id, zipfilename))
    os.remove(lock_file)
    logger.sys.debug("DownloadBoard move over, delete lock")
    dtime = "%.2f" %(time.time() - stime)
    #发送邮件提醒
    if email_check(email):
        remind = "mailto:{}".format(email)
        message = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/><style>a{text-decoration: none}</style></head><body><table style="width:550px;"><tr><td style="padding-top:10px; padding-left:5px; padding-bottom:5px; border-bottom:1px solid #D9D9D9; font-size:16px; color:#999;">SaintIC EauDouce</td></tr><tr><td style="padding:20px 0px 20px 5px; font-size:14px; line-height:23px;">你好！<br>图片下载完成，地址是<a href="%s" target="_blank">%s</a><br></td></tr><tr><td style="padding-top:5px; padding-left:5px; padding-bottom:10px; border-top:1px solid #D9D9D9; font-size:12px; color:#999;">此为系统邮件，请勿回复<br/>请保管好您的邮箱，避免账户被他人盗用<br/><br/>如有任何疑问，可查看网站帮助 <a target="_blank" href="https://www.saintic.com">https://www.saintic.com</a></td></tr></table></body></html>' %(downloadUrl, downloadUrl)
        sendmail = SendMail()
        try:
            result = sendmail.SendMessage(to_addr=email, subject=u"%s下载完成提醒" %(u"花瓣网画板" if site == 1 else u"堆糖网专辑"), formatType="html", message=message)
            if result["success"]:
                remind += ":Success"
            else:
                remind += ":Failure:" + result.get("msg", "")
            _sb.mysql_write.update("update plugin_crawlhuaban set remind=%s where board_id=%s and filename=%s", remind, board_id, zipfilename)
        except Exception,e:
            logger.sys.error(e, exc_info=True)
    try:
        _sb.mysql_write.update("update plugin_crawlhuaban set status=1,size=%s,dtime=%s where board_id=%s and filename=%s", size, dtime, board_id, zipfilename)
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

def CountDownloadBoard(site, version, total_number, pin_number, board_id, user_id, downloadMethod, atime, user_ip, user_agent):
    try:
        if user_agent:
            # 解析User-Agent
            uap = user_agents_parse(user_agent)
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
        else:
            browserType, browserDevice, browserOs, browserFamily = "", "", "", "", ""
        _sb.mysql_write.insert("insert into plugin_crawlhuaban_clicklog (site,user_id,board_id,pin_number,total_number,atime,version,download_method,user_ip,user_area,user_agent,browser_type,browser_device,browser_os,browser_family) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", site, user_id, board_id, pin_number, total_number, atime, version, downloadMethod, user_ip, getIpArea(user_ip), user_agent, browserType, browserDevice, browserOs, browserFamily)
    except Exception,e:
        logger.sys.error(e, exc_info=True)

