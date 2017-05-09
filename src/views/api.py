# -*- coding: utf8 -*-

import time
from torndb import IntegrityError
from flask import request, g, Blueprint, abort
from flask_restful import Api, Resource
from utils.tool import logger

class Blog(Resource):

    def get(self):
        """
        1.limit(int), 限制列出数据数量，默认None，全局参数。
        2.sort(str), 数据排序, desc、asc，默认desc，全局参数。
        3.blogId(int), 查询某一个id的文章, 独立参数。
        4.get_catalog_list(bool), 列出博客所有目录，独立参数。
        5.get_tags_list(bool),
        6.get_catalog_data(str), 查询博客某目录下的limit个文章。
        7.get_sources_data(str), 查询博客某来源下的limit个文章，1是原创，2是转载，3是翻译。
        8.get_index(bool),仅仅查询所有博客标题、ID、创建时间。
        9.get_user(str),查询某用户的所有博客。
        10.get_update_data(bool)，查询更新过的文章
        11.get_top_data(bool)，查询置顶文章
        12.get_recommend_data(bool)，查询推荐文章
        13.get_tags_data(str)，查询某标签下的文章
        """
        limit  = request.args.get('limit', None)
        sort   = request.args.get('sort', 'desc')
        blogId = request.args.get('blogId', None)

        get_catalog_data  = request.args.get("get_catalog_data")
        get_sources_data  = request.args.get("get_sources_data")
        get_tags_data     = request.args.get("get_tags_data")

        get_update_data   = True if request.args.get("get_update_data") in ("true", "True", True) else False
        get_top_data      = True if request.args.get("get_top_data") in ("true", "True", True) else False
        get_recommend_data= True if request.args.get("get_recommend_data") in ("true", "True", True) else False

        get_tags_list    = True if request.args.get("get_tags_list") in ("true", "True", True) else False
        get_catalog_list = True if request.args.get("get_catalog_list") in ("true", "True", True) else False

        get_user  = request.args.get("get_user")
        get_index = True if request.args.get("get_index") in ("true", "True", True) else False

        if blogId:
           return g.api.blog_get_id(blogId)

        if get_catalog_data:
            return g.api.blog_get_catalog_data(get_catalog_data, sort, limit)
        if get_sources_data:
            return g.api.blog_get_sources_data(get_sources_data, sort, limit)
        if get_tags_data:
            return g.api.blog_get_tag_data(get_tags_data, sort)

        if get_update_data:
            return g.api.blog_get_update_data(sort, limit)
        if get_top_data:
            return g.api.blog_get_top_data(sort, limit)
        if get_recommend_data:
            return g.api.blog_get_recommend_data(sort, limit)

        if get_tags_list:
            return g.api.blog_get_tags_list()
        if get_catalog_list:
            return g.api.blog_get_catalog_list()

        if get_user:
            return g.api.blog_get_user_blog(get_user, sort, limit)
        if get_index:
            page   = int(request.args.get("page", 0))
            length = int(request.args.get("length", 5))
            return g.api.blog_get_single_index(sort, limit, page, length)

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
        logger.debug(data)
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
            logger.debug(data)
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
        blogId = request.args.get("blogId")
        action = request.args.get("action")
        value  = request.args.get("value", "true")

        if action == "recommend":
            return g.api.misc_set_recommend(blogId, value)
        elif action == "top":
            return g.api.misc_set_top(blogId, value)
        else:
            return {"msg": "illegal parameter action", "code": -1}

class User(Resource):

    def get(self):
        """Public func, no token, with url args:
        1. num, 展现的数量,默认是10条,可为all
        2. username|email, 用户名或邮箱，数据库主键，唯一。

        返回数据样例，{'msg':'success or error(errmsg)', 'code':'result code', 'data':data, 'success': True or False}
        """
        res = {"code": 200, "msg": None, "data": None}
        username     = request.args.get("username")
        getalluser   = True if request.args.get("getalluser") in ("True", "true", True) else False
        getadminuser = True if request.args.get("getadminuser") in ("True", "true", True) else False

        logger.info(res)
        return res

    def post(self):
        """login and registry, with url args:
        1. action=log/reg, default is log;

        post data:
        1. username,
        2. password,
        3. email
        """
        NULL     = None
        res      = {"url": request.url, "msg": None, "success": False}
        username = request.form.get("username")
        password = request.form.get("password")
        email    = request.form.get("email", NULL)
        action   = request.args.get("action") #log or reg (登录or注册)

        #chck username and password value
        if not username or not password:
            res.update(msg="Invaild username or password", code=10001)
            logger.info(res)
            return res

        #check username and password length
        if 5 <= len(username) < 30 and 5 <= len(password) < 30:
            MD5password = md5(password)
        else:
            res.update({'msg': 'username or password length requirement is greater than or equal to 5 less than 30', 'code': 10002})
            logger.warn(res)
            return res

        #check username pattern
        if not user_pat.match(username):
            res.update({'msg': 'username is not valid', 'code': 10003})
            logger.warn(res)
            return res

        if email and mail_pat.match(email) == None:
            res.update({'msg': "email format error", 'code': 10004})
            logger.warn(res)
            return res

        #Start Action with (log, reg)
        if action == 'SignIn':
            logger.debug(RegisteredUser())
            logger.debug("MD5password: %s, DBpassword: %s, username: %s" %(MD5password, RegisteredUserInfo(username).get("lauth_password"),username))
            if username in RegisteredUser():
                if MD5password == RegisteredUserInfo(username).get("lauth_password"):
                    res.update({'msg': 'Password authentication success at sign in', 'code': 0, "success": True})
                else:
                    res.update({'msg': 'Password authentication failed at sign in', 'code': 10005, "success": False})
            else:
                res.update({'msg':'username not exists', 'code': 10006})
            logger.info(res)
            return res

        elif action == 'SignUp':
            try:
                AuthSQL = "INSERT INTO LAuth (lauth_username, lauth_password) VALUES(%s, %s)"
                logger.info(AuthSQL)
                mysql.insert(AuthSQL, username, MD5password)
                UserSQL = "INSERT INTO User (username, email, time, avatar) VALUES(%s, %s, %s, %s)"
                mysql.insert(UserSQL, username, email, get_today(), "/static/img/avatar/default.jpg")
            except IntegrityError, e:
                logger.error(e, exc_info=True)
                res.update({'msg': 'username already exists, cannot be registered!', 'code': 10007})
                logger.warn(res)
                return res
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(msg="server error", code=-1)
                logger.error(res)
                return res
            else:
                res.update({'code': 0, 'msg': 'Sign up success', "success": True})
                logger.info(res)
                return res

        else:
            res.update({'msg': 'Request action error', 'code': 10008})
            logger.info(res)
            return res

    def delete(self):
        #sql = "DELETE FROM user WHERE username=%s"
        #logger.info({"User:delete:SQL": sql})
        return {}

    def put(self):
        """Update user profile"""
        
        if request.args.get("ChangeType") == "password":
            return g.api.user_update_password(request.form.get("username"), request.form.get("OldPassword"), request.form.get("NewPassword"))
        elif request.args.get("ChangeType") == "profile":
            data = { k:v for k,v in request.form.iteritems() if k in ("email", "cname", "avatar", "motto", "url", "weibo", "github", "gender") }
            return g.api.user_update_profile(username=request.form.get("username", None), **data)

class Sys(Resource):

    def get(self):
        "查询系统数据"

        res   = {"code": 200, "msg": None, "data": None}
        query = request.args.get("q", request.args.get("query", None))

        if query == "notice":
            sql = "SELECT msg FROM sys_notice"
            try:
                data = mysql.query(sql)
                logger.info("query notice data with sql: " + sql)
            except Exception,e:
                logger.error(e)
            else:
                res.update(data=data)

        logger.info(res)
        return res

class Author(Resource):

    def get(self):
        return g.api.get_apply_author()

    def post(self):
        return g.api.post_apply_author(request.args.get("username"))

class Comment(Resource):

    def get(self):
        """
        查询blogId的评论数
        """
        return g.api.misc_get_commend(request.args.get("blogId"))

class Cache(Resource):

    def get(self):
        data = g.cache.get_cache_blog(request.args.get("blogId"))
        g.hitCache = True if data else False
        return data

    def post(self):
        return g.cache.post_cache_blog(request.args.get("blogId"))

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)
api.add_resource(Blog, '/blog', '/blog/', endpoint='blog')
api.add_resource(Misc, '/misc', '/misc/', endpoint='misc')
api.add_resource(User, '/user', '/user/', endpoint='user')
api.add_resource(Sys, '/sys', '/sys/', endpoint='sys')
api.add_resource(Comment, '/comment', '/comment/', endpoint='comment')
api.add_resource(Cache, "/cache/", "/cache", endpoint="cache")
api.add_resource(Author, "/author/", "/author", endpoint="author")
