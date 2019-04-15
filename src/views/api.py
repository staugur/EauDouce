# -*- coding: utf-8 -*-
"""
    EauDouce.views.api
    ~~~~~~~~~~~~~~

    Foreground interface view.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import time
from torndb import IntegrityError
from flask import request, g, Blueprint, abort
from flask_restful import Api, Resource
from utils.tool import logger
from utils.Signature import Signature
from utils.web import apilogin_required

sign = Signature()

class Blog(Resource):

    def post(self):
        """ 创建博客文章接口 """
        if g.username not in g.api.user_get_authors().get("data"):
            return {"code": 403, "msg": "Permission denied, not author"}, 403

        data = dict(
            title   = request.form.get('title'),
            content = request.form.get('content'),
            tag     = request.form.get("tag"),
            catalog = request.form.get("catalog", "未分类"),
            sources = request.form.get("sources", "原创"),
            author  = request.form.get("author", "admin")
        )
        logger.sys.debug(data)
        return g.api.blog_create(**data)

    def put(self):
        """ 更新博客文章接口 """
        if g.username == request.form.get("author") or g.username in g.api.user_get_admins().get("data"):#可能伪造author
            data = dict(
                title   = request.form.get('title'),
                content = request.form.get('content'),
                tag     = request.form.get("tag"),
                catalog = request.form.get("catalog", "未分类"),
                sources = request.form.get("sources", "原创"),
                author  = request.form.get("author", "admin"),
                blogId  = request.form.get("blogId")
            )
            logger.sys.debug(data)
            return g.api.blog_update(**data)
        else:
            return {"code": 403, "msg": "Permission denied"}, 403

    def delete(self):
        """ 删除博客文章接口 """

        blogId = request.args.get("blogId")
        if g.username in g.api.user_get_admins().get("data"):
            return g.api.blog_delete(blogId)
        else:
            return abort(403)

class Misc(Resource):

    def post(self):
        """
        设置或取消->
        推荐文章: Recommended articles 
        置顶文章: Sticky articles 
        """
        action = request.args.get("action")
        blogId = request.args.get("blogId")
        value  = request.args.get("value", "true")

        if action == "recommend":
            return g.api.misc_set_recommend(blogId, value)
        elif action == "top":
            return g.api.misc_set_top(blogId, value)
        elif action == "BaiduActivePush":
            """ 百度主动推送(实时)插件 """
            # 要推送的URL地址，大部分情况下应该是request.base_url
            pushUrl = request.form.get("pushUrl")
            # 是否原创文章
            original = True if request.form.get("original") in ("1", "true", "True", True) else False
            return g.api.misc_BaiduActivePush(pushUrl, original)
        else:
            return {"msg": "illegal parameter action", "code": -1}

class Sys(Resource):

    def post(self):

        query = request.args.get("q", request.args.get("query", None))

        if query == "notice":
            return g.api.post_sys_notice(request.form.get("noticeMsg"))
        if query == "friendlink":
            return g.api.post_sys_friendlink(request.form.get("link"), request.form.get("title"))

    def delete(self):

        query = request.args.get("q", request.args.get("query", None))

        if query == "notice":
            return g.api.delete_sys_notice(request.form.get("noticeId"))
        if query == "friendlink":
            return g.api.delete_sys_friendlink(request.form.get("friendlinkId"))

    def put(self):

        query = request.args.get("q", request.args.get("query", None))
        if query == "configure":
            data = { k:v for k,v in request.form.iteritems() if k in ("about_awi", "about_ww", "about_address", "about_phone", "about_email", "about_beian", "seo_keywords", "seo_description", "site_title", "site_feedname", "applet", "status_url") }
            return g.api.update_sys_configure(**data)


class WechatApplet(Resource):
    """ 小程序专属接口 """

    @sign.signature_required
    def post(self):
        Action = request.args.get("Action")
        if Action == "AccessUserLog":
            logger.sys.debug(request.form)
            return g.api.post_applet_users(
                avatarUrl=request.form.get("avatarUrl"),
                country=request.form.get("country"),
                province=request.form.get("province"),
                city=request.form.get("city"),
                gender=request.form.get("gender"),
                nickName=request.form.get("nickName"),
            )

    @sign.signature_required
    def get(self):
        Action = request.args.get("Action")
        if Action == "get_index":
            sort   = request.args.get('sort', 'desc')
            limit  = request.args.get('limit', None)
            page   = int(request.args.get("page", 0))
            length = int(request.args.get("length", 5))
            return g.api.blog_get_single_index(sort, limit, page, length)
        elif Action == "get_banner":
            return g.api.get_banner()
        elif Action == "get_blogId":
            blogId = int(request.args.get('blogId'))
            return g.api.blog_get_id(blogId)
        elif Action == "get_top":
            sort   = request.args.get('sort', 'desc')
            limit  = request.args.get('limit', None)
            return g.api.blog_get_top_data(sort, limit)

class NovelView(Resource):
    """小说接口"""

    #@sign.signature_required
    def get(self):
        res = dict(code=-1)
        Action = request.args.get("Action")
        if Action == "getBooks":
            res = g.api.novel_get_books()
        elif Action == "getChapters":
            book_id = request.args.get("bood_id")
            res = g.api.novel_get_chapters(book_id)
        elif Action == "getChapterDetail":
            chapter_id = request.args.get("chapter_id")
            res = g.api.novel_get_chapter_detail(chapter_id)
        return res

    @apilogin_required
    def post(self):
        res = dict(code=-1)
        if not g.uid in g.api.user_get_admins()["data"]:
            res.update(msg="Administrator privileges are required")
            return res
        Action = request.args.get("Action")
        if Action == "addBook":
            name = request.form.get("name")
            summary = request.form.get("summary")
            cover = request.form.get("cover")
            link = request.form.get("link") or ""
            res = g.api.novel_post_book(name, summary, cover, link)
        elif Action == "addChapter":
            book_id = request.form.get("bood_id")
            title = request.form.get("title")
            content = request.form.get("content")
            res = g.api.novel_post_chapter(book_id, title, content)
        return res

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)
api.add_resource(Blog, '/blog', '/blog/', endpoint='blog')
api.add_resource(Misc, '/misc', '/misc/', endpoint='misc')
api.add_resource(Sys, '/sys', '/sys/', endpoint='sys')
api.add_resource(WechatApplet, '/wechatapplet', '/wechatapplet/', endpoint='wechatapplet')
api.add_resource(NovelView, '/novel', '/novel/', endpoint='novel')
