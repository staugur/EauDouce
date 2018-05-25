# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.CrawlHuaban
    ~~~~~~~~~~~~~~

    抓取花瓣网图片

    :copyright: (c) 2018 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from libs.base import PluginBase
import os
import json
from config import PLUGINS
from utils.tool import logger, get_current_timestamp, timestamp_after_timestamp, timestamp_to_timestring
from utils.qf import DownloadBoard, DownloadBoardDelete
from flask import Blueprint, jsonify, request, make_response, url_for, send_from_directory

__name__ = "CrawlHuaban"
__description__ = "抓取花瓣网图片并压缩提供下载"
__author__ = "Mr.tao"
__version__ = "0.1"
__license__ = "MIT"
if PLUGINS["CrawlHuaban"] in ("true", "True", True):
    __state__ = "enabled"
else:
    __state__ = "disabled"

basedir = os.path.dirname(os.path.abspath(__file__))
logger.sys.debug("CrawlHuaban basedir: {}".format(basedir))
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
        board_id = str(request.args.get("board_id", ""))
        # 下载文件名
        filename = request.args.get("filename")
        if board_id and filename:
            # 下载文件存放目录
            directory = os.path.join(basedir, board_id)
            logger.sys.debug("Want to download a file with directory: {0}, filename: {1}".format(directory, filename))
            headers = ("Content-Disposition", "attachment;filename={}".format(filename))
            if os.path.isfile(os.path.join(directory, filename)):
                response = make_response(send_from_directory(directory=directory, filename=filename, as_attachment=True))
                response.headers[headers[0]] = headers[1]
            else:
                response = make_response("Not Found File")
        else:
            response = make_response("Invalid Download Request")
        return response
    else:
        res = dict(success=False, msg=None)
        try:
            board_id = str(request.form.get("board_id", ""))
            board_pins = json.loads(request.form.get("pins"))
            if board_id and board_pins:
                if not isinstance(board_pins, (list, tuple)):
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            res.update(msg="Invalid data")
        except Exception, e:
            logger.sys.error(e, exc_info=True)
            res.update(msg="Unknown error, please contact staugur@saintic.com, thanks!")
        else:
            logger.sys.debug("dir: {}, board_id: {}, board_pins number: {}, type: {}, result: {}".format(basedir, board_id, len(board_pins), type(board_pins), board_pins))
            filename = "{}_{}".format(board_id, get_current_timestamp())
            pb = PluginBase()
            pb.asyncQueueHigh.enqueue(DownloadBoard, basedir, board_id, filename, board_pins)
            res.update(success=True, downloadUrl=url_for("CrawlHuaban.index", board_id=board_id, filename="{}.zip".format(filename), _external=True), expireTime=timestamp_to_timestring(timestamp_after_timestamp(hours=24)))
        logger.sys.info(res)
        return jsonify(res)


def getPluginClass():
    return CrawlHuabanMain


class CrawlHuabanMain(PluginBase):
    """ 抓取花瓣网画板图片 """

    def register_bep(self):
        """ 注册一个查询uv接口 """
        return {"prefix": "/CrawlHuaban", "blueprint": CrawlHuabanBlueprint}
