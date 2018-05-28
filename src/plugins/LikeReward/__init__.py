# -*- coding: utf-8 -*-
"""
    EauDouce.plugins.LikeReward
    ~~~~~~~~~~~~~~

    点赞打赏组件

    :copyright: (c) 2018 Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

#: Importing these two modules is the first and must be done.
#: 首先导入这两个必须模块
from __future__ import absolute_import
from libs.base import PluginBase
#: Import the other modules here, and if it's your own module, use the relative Import. eg: from .lib import Lib
#: 在这里导入其他模块, 如果有自定义包目录, 使用相对导入, 如: from .lib import Lib
from config import PLUGINS
from utils.tool import get_current_timestamp
from flask import Blueprint, request, jsonify, g

#：Your plug-in name must be consistent with the plug-in directory name.
#：你的插件名称，必须和插件目录名称等保持一致.
__name__        = "LikeReward"
#: Plugin describes information. What does it do?
#: 插件描述信息,什么用处.
__description__ = "点赞打赏组件"
#: Plugin Author
#: 插件作者
__author__      = "Mr.tao <staugur@saintic.com>"
#: Plugin Version
#: 插件版本
__version__     = "0.2" 
#: Plugin Url
#: 插件主页
__url__         = "https://www.saintic.com"
#: Plugin License
#: 插件许可证
__license__     = "MIT"
#: 插件状态, enabled、disabled, 默认enabled
if PLUGINS["LikeReward"] in ("true", "True", True):
    __state__   = "enabled"
else:
    __state__   = "disabled"

class LikeApi(PluginBase):
    """点赞接口，每用户只能对文章点赞一次，可以取消。
    已点赞则显示取消赞按钮；
    未点赞则显示点赞按钮。
    """

    def __init__(self):
        super(LikeApi, self).__init__()
        self.genIndexKey = lambda blogId: "EauDouce:LikeCount:Sum:{}".format(blogId)
        self.genSecondKey = lambda blogId, userId: "EauDouce:LikeCount:Entry:{}:{}".format(blogId, userId)

    def check(self, blogId):
        """检测blogId参数"""
        try:
            blogId = int(blogId)
        except:
            return False
        else:
            return True

    def like(self, blogId, userId, loginStatus):
        """点赞
        @param blogId int: 博客id
        @param userId str: 登录时用户id，未登录时浏览器指纹
        @param loginStatus int: 登录状态，0未登录 1已登录
        数据规则:
        1. 每个blogId是一个set，set中存userId。
        2. 每个userId是一个hash，格式是：{userId: xx, blogId: xx, loginStatus: 0未登录、1已登录, likeTime: 时间戳}
        3. 取消赞即删除userId及hash数据
        """
        res = dict(code=1, msg=None)
        if self.has(blogId, userId):
            res.update(code=0, msg="Already praised")
        else:
            if self.check(loginStatus) and loginStatus in (0, 1):
                key = self.genIndexKey(blogId)
                pipe = self.redis.pipeline()
                pipe.sadd(key, userId)
                pipe.hmset(self.genSecondKey(blogId, userId), dict(userId=userId, blogId=blogId, loginStatus=loginStatus, likeTime=get_current_timestamp()))
                try:
                    pipe.execute()
                except Exception,e:
                    self.logger.error(e, exc_info=True)
                    res.update(code=2)
                else:
                    res.update(code=0)
            else:
                res.update(msg="Invalid parameters", code=3)
        return res

    def cancel(self, blogId, userId):
        """取消点赞
        @param blogId int: 博客id
        @param userId str: 登录时用户id，未登录时浏览器指纹
        """
        res = dict(code=1, msg=None)
        if self.has(blogId, userId):
            pipe = self.redis.pipeline()
            pipe.delete(self.genSecondKey(blogId, userId))
            pipe.srem(self.genIndexKey(blogId), userId)
            try:
                pipe.execute()
            except Exception,e:
                self.logger.error(e, exc_info=True)
                res.update(code=2)
            else:
                res.update(code=0)
        else:
            res.update(code=0, msg="Unliked or incorrect parameters")
        return res

    def has(self, blogId, userId):
        """blogId是否有userId已点赞数据，
        返回True即已经点赞；否则未点赞
        """
        if self.check(blogId) and userId:
            key = self.genIndexKey(blogId)
            if self.redis.sismember(key, userId):
                return True
        return False

    def query(self, blogId, userId=None):
        """查询blogId的点赞数据
        当userId为真时，查询其对应数据；否则查询blogId所有数据
        """
        res = dict(code=1, msg=None)
        if self.check(blogId):
            key = self.genIndexKey(blogId)
            try:
                data = [ self.redis.hgetall(self.genSecondKey(blogId, userId)) for userId in list(self.redis.smembers(key)) if userId ]
            except Exception,e:
                self.logger.error(e, exc_info=True)
                res.update(msg="Like failed", code=2)
            else:
                res.update(code=0, data=data)
        else:
            res.update(msg="Invalid parameters", code=3)
        return res

    def queryAll(self):
        """查询所有blogId数据"""
        res = dict(code=1, msg=None)
        if self.redis.ping():
            data = {}
            for key in self.redis.keys("EauDouce:LikeCount:Sum:*"):
                blogId = key.split(":")[-1]
                data.update({blogId: [ self.redis.hgetall(self.genSecondKey(blogId, userId)) for userId in list(self.redis.smembers(key)) if userId ]})
            res.update(data=data, code=0)
        else:
            res.update(code=2, msg="Service Unreachable")
        return res

plugin_blueprint = Blueprint("LikeReward", "LikeReward")
@plugin_blueprint.route("/", methods=["GET", "POST"])
def index():
    """统计点赞数量，规则：
    1. 游客用户，采用fingerprintjs2，生成浏览器唯一指纹，每个指纹只能点赞一次。
    2. 登录用户只能点赞一次。
    3. 点击一次赞，点击两次取消赞。
    """
    res = dict(code=-1, msg=None)
    Action = request.args.get("Action")
    Likeapi = LikeApi()
    if request.method == "GET":
        blogId = request.args.get("blogId")
        userId = request.args.get("userId")
        if Action == "query":
            res = Likeapi.query(blogId, userId)
        elif Action == "has":
            res = dict(has=Likeapi.has(blogId, userId))
        elif Action == "queryAll":
            res = Likeapi.queryAll()
    else:
        blogId = request.form.get("blogId")
        userId = request.form.get("userId")
        if Action == "like":
            res = Likeapi.like(blogId, userId, 1 if g.signin else 0)
        elif Action == "cancel":
            res = Likeapi.cancel(blogId, userId)
    Likeapi.logger.debug(res)
    return jsonify(res)

#: 返回插件主类
def getPluginClass():
    return LikeRewardMain

class LikeRewardMain(PluginBase):
    
    __doc__ = __description__

    def register_tep(self):
        return {"blog_show_content_include": "LikeReward.html", "blog_show_script_include": "LikeRewardJS.html"}

    def register_bep(self):
        """注册蓝图入口, 返回蓝图路由前缀及蓝图名称"""
        bep = {"prefix": "/LikeReward", "blueprint": plugin_blueprint}
        return bep
