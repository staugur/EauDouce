# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.CrawlHuaban
    ~~~~~~~~~~~~~~

    抓取花瓣、堆糖图片

    :copyright: (c) 2018 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from libs.base import PluginBase
import os, json
from config import PLUGINS
from utils.qf import DownloadBoard, DownloadBoardAddTimes, CountDownloadBoard
from utils.tool import logger, get_current_timestamp, timestamp_after_timestamp, timestamp_to_timestring, email_check
from flask import Blueprint, jsonify, request, make_response, url_for, send_from_directory
from werkzeug import secure_filename

__plugin_name__  = "CrawlHuaban"
__description__ = "抓取花瓣、堆糖图片并压缩提供下载"
__author__ = "Mr.tao"
__version__ = "0.3.0"
__license__ = "MIT"
if PLUGINS["CrawlHuaban"] in ("true", "True", True):
    __state__ = "enabled"
else:
    __state__ = "disabled"

pb = PluginBase()
basedir = os.path.dirname(os.path.abspath(__file__))
CrawlHuabanBlueprint = Blueprint("CrawlHuaban", "CrawlHuaban")
@CrawlHuabanBlueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        """ 下载图片压缩文件
        :board_id(str):  下载分类(子)目录，比如attachment、script
        :filename(str): 下载的实际文件(不需要目录，目录由catalog指定)，包含扩展名
        当前目录是EauDouce/src/plugins/CrawlHuaban/，作为根。
        1. 以board_id为子，进去子目录下载保存；
        2. 返回根目录，压缩board_id目录成文件，再移动到board_id下。
        """
        # 下载画板
        board_id = secure_filename(str(request.args.get("board_id", "")))
        # 下载文件名
        filename = secure_filename(request.args.get("filename", ""))
        if board_id and filename:
            # 下载文件存放目录
            directory = os.path.join(basedir, board_id)
            logger.sys.debug("Want to download a file with directory: {0}, filename: {1}".format(directory, filename))
            headers = ("Content-Disposition", "attachment;filename={}".format(filename))
            if os.path.isfile(os.path.join(directory, filename)):
                pb.asyncQueue.enqueue_call(func=DownloadBoardAddTimes, args=(board_id, filename, get_current_timestamp()))
                response = make_response(send_from_directory(directory=directory, filename=filename, as_attachment=True))
                response.headers[headers[0]] = headers[1]
            else:
                response = make_response("Not Found File")
        else:
            response = make_response("Invalid Download Request")
        return response
    else:
        # 关于tip，可以是text或html格式，前端页面直接显示这个值内容，用于额外提示信息，若无提示，保持为空字符
        res = dict(success=False, msg=None, tip='')
        try:
            #site站点，花瓣网1、堆糖网2
            site = int(request.form.get("site", 1))
            #version脚本版本
            version = request.form.get("version", "")
            #以下board同album，不区分
            board_id = str(request.form.get("board_id", ""))
            board_pins = json.loads(request.form.get("pins"))
            board_total = int(request.form.get("board_total", 0))
            email = request.form.get("email")
            if board_id and board_pins:
                if not isinstance(board_pins, (list, tuple)):
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            res.update(msg=u"无效数据格式")
        except Exception, e:
            logger.sys.error(e, exc_info=True)
            res.update(msg=u"未知错误, 请联系作者staugur@saintic.com反馈，谢谢!")
        else:
            logger.sys.debug("dir: {}, site: {}, version: {}, board_id: {}, board_pins number: {}".format(basedir, site, version, board_id, len(board_pins)))
            #将site+board_id存入redis，限定时间内不允许重复下载
            key = "EauDouce:CrawlHuaban:{site}:{board_id}".format(site=site, board_id=board_id)
            hasKey = False
            try:
                hasKey = pb.redis.exists(key)
            except Exception,e:
                logger.sys.error(e, exc_info=True)
            if hasKey:
                data = pb.redis.hgetall(key)
                res.update(msg=u'当前画板下载中，链接是<a href="{}" target="_blank" title="请点击打开新页面或手动复制链接">{}</a>。温馨提示，5分钟内请勿重复对同一个画板使用远程下载服务！'.format(data["downloadUrl"], data["downloadUrl"]))
            else:
                ctime = get_current_timestamp()
                etime = timestamp_after_timestamp(hours=24)
                filename = "{}_{}.zip".format(site, ctime)
                expireTime = timestamp_to_timestring(etime)
                downloadUrl = url_for("CrawlHuaban.index", board_id=board_id, filename=filename, _external=True)
                pipe = pb.redis.pipeline()
                pipe.hmset(key, dict(downloadUrl=downloadUrl, expireTime=expireTime))
                pipe.expire(key, 300)
                # 设置彩蛋功能区
                eggKey = "EauDouce:CrawlHuaban:HF:{}".format(downloadUrl)
                pipe.hset(eggKey, "remind", email)
                pipe.expire(eggKey, 24 * 3600)
                try:
                    pipe.execute()
                except Exception,e:
                    logger.sys.error(e, exc_info=True)
                finally:
                    pb.asyncQueueHigh.enqueue_call(func=DownloadBoard, args=(basedir, board_id, filename, board_pins, board_total, ctime, etime, version, site, request.headers.get('X-Real-Ip', request.remote_addr), request.headers.get("User-Agent"), downloadUrl), timeout=3600)
                    res.update(success=True, downloadUrl=downloadUrl, expireTime=expireTime)
                    # 更新邮件发送的提示
                    if email:
                        if email_check(email):
                            res.update(tip=u"<br>您已设置邮箱，当前画板后端下载完成后将发送邮件提醒，请注意查收！")
                        else:
                            res.update(tip=u"<br>您已设置邮箱，但邮箱格式错误，将不会发送邮件提醒。")
        logger.sys.info(res)
        return jsonify(res)

@CrawlHuabanBlueprint.route("/putEgg", methods=["POST"])
def putEgg():
    if request.method == "POST":
        res = dict(success=False, msg=None, tip='')
        try:
            # 必选参数-下载链接
            downloadUrl = request.form.get("downloadUrl")
            # 可选参数
            email = request.form.get("email")
            if not downloadUrl:
                raise ValueError
        except ValueError:
            res.update(msg="Invalid downloadUrl")
        except Exception:
            res.update(msg="Unknown error")
        else:
            eggKey = "EauDouce:CrawlHuaban:HF:{}".format(downloadUrl)
            eggData = pb.redis.hgetall(eggKey)
            if not int(eggData.get("status", 0)) in (1, 2):
                pipe = pb.redis.pipeline()
                if email:
                    if email_check(email):
                        pipe.hset(eggKey, "remind", email)
                        res.update(tip=u"您已设置邮箱，当前画板后端下载完成后将发送邮件提醒，请注意查收！")
                    else:
                        res.update(tip=u"您已设置邮箱，但邮箱格式错误，将不会发送邮件提醒。")
                try:
                    pipe.execute()
                except Exception,e:
                    logger.sys.error(e, exc_info=True)
                    res.update(msg="System is abnormal")
                else:
                    res.update(success=True)
            else:
                res.update(tip=u'下载已完成，<a href="%s">点击下载</a>' %downloadUrl, success=True)
        logger.sys.info(res)
        return jsonify(res)

@CrawlHuabanBlueprint.route("/putClick", methods=["POST"])
def putClick():
    if request.method == "POST":
        res = dict(success=False, msg=None)
        try:
            #site站点，花瓣网1、堆糖网2
            site = int(request.form.get("site", 0))
            #version脚本版本
            version = request.form.get("version", "")
            #以下board同album，不区分
            total_number = int(request.form.get("total_number", 0))
            pin_number = int(request.form.get("pin_number", 0))
            board_id = str(request.form.get("board_id", ""))
            user_id = str(request.form.get("user_id", ""))
            downloadMethod = int(request.form.get("downloadMethod", "0"))
            if not board_id:
                raise ValueError
        except ValueError:
            res.update(msg="Invalid format")
        except Exception:
            res.update(msg="Unknown error")
        else:
            pb.asyncQueue.enqueue_call(func=CountDownloadBoard, args=(site, version, total_number, pin_number, board_id, user_id, downloadMethod, get_current_timestamp(), request.headers.get('X-Real-Ip', request.remote_addr), request.headers.get("User-Agent")))
            res.update(success=True)
        logger.sys.info(res)
        return jsonify(res)


def getPluginClass():
    return CrawlHuabanMain


class CrawlHuabanMain(PluginBase):
    """ 抓取花瓣网画板图片 """

    def register_bep(self):
        """ 注册一个查询uv接口 """
        return {"prefix": "/CrawlHuaban", "blueprint": CrawlHuabanBlueprint}
