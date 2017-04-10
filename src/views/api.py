# -*- coding: utf8 -*-

import time
from torndb import IntegrityError
from flask import request, g, Blueprint
from flask_restful import Api, Resource
from utils.tool import logger

class Blog(Resource):

    def get(self):
        """
        1.num|limit(int, str), 限制列出数据数量，另外可设置为all，列出所有blog， 全局参数。
        2.sort(str), 数据排序, 全局参数。
        3.blogId(int), 查询某一个id的文章, 独立参数。
        4.get_catalog_list(bool), 列出博客所有目录，独立参数。
        5.get_sources_list(bool), 列出博客所有类型，独立参数。
        6.get_catalog_data(str), 查询博客某目录下的num个文章。
        7.get_sources_data(str), 查询博客某类型下的num个文章。
        8.get_index_only(bool),仅仅查询所有博客标题、ID、创建时间。
        9.get_user_blog(str),查询某用户的所有博客。
        10.get_tags_list(bool),
        """
        res    = {"url": request.url, "msg": None, "data": None, "code": 0}
        num    = request.args.get('num', request.args.get('limit', 10))
        LIMIT  = '' if num in ("all", "All") else "LIMIT " + str(num)
        sort   = request.args.get('sort', 'desc')
        blogId = request.args.get('blogId')
        get_catalog_list = True if request.args.get("get_catalog_list") in ("true", "True", True) else False
        get_sources_list = True if request.args.get("get_sources_list") in ("true", "True", True) else False
        get_catalog_data = request.args.get("get_catalog_data")
        get_sources_data = request.args.get("get_sources_data")
        get_index_only   = True if request.args.get("get_index_only") in ("true", "True", True) else False
        get_user_blog    = request.args.get("get_user_blog")
        get_tags_list    = True if request.args.get("get_tags_list") in ("true", "True", True) else False
        get_tags_data    = request.args.get("get_tags_data")
        get_update_data  = True if request.args.get("get_update_data") in ("true", "True", True) else False
        get_recommend_data=True if request.args.get("get_recommend_data") in ("true", "True", True) else False
        get_top_data     = True if request.args.get("get_top_data") in ("true", "True", True) else False

        if get_recommend_data:
            return res

        if get_top_data:
            return res

        if get_tags_data:
            return res

        if get_tags_list:
            return g.api.blog_get_tags_list()

        if get_index_only:
            return res

        if get_update_data:
            return res

        if get_catalog_list:
            return res

        if get_sources_list:
            return res

        if get_catalog_data:
            return res

        if get_sources_data:
            return res

        if get_user_blog:
            return res

        return res

    def post(self):
        """ 创建博客文章接口 """
        return g.api.blog_create(request.form)

    def put(self):
        """ 更新博客文章接口 """
        return g.api.blog_update(request.form)

class Misc(Resource):

    def post(self):
        """
        设置->
        推荐文章: Recommended articles 
        置顶文章: Sticky articles 
        """
        res    = {"url": request.url, "msg": None, "success": False, "code": 0}
        blogId = request.args.get("blogId")
        action = request.args.get("action")
        value  = request.args.get("value", "true")
        logger.info("blogId: %s, action: %s, value: %s" %(blogId, action, value) )

        #check params
        if not value in ("true", "True", True, "false", "False", False):
            res.update(msg="illegal parameter value", code=-1)
        try:
            blogId = int(blogId)
        except:
            res.update(msg="illegal parameter blogId", code=-1)
        if not action in ("recommend", "top"):
            res.update(msg="illegal parameter action", code=-1)
        if res['msg']:
            logger.info(res)
            return res

        try:
            sql = "UPDATE blog_article SET update_time='%s',%s='%s' WHERE id=%d" %(get_today(), action, value, blogId)
            logger.info(sql)
            mysql.update(sql)
        except Exception,e:
            logger.error(e, exc_info=True)
            res.update(success=False)
        else:
            res.update(success=True)

        logger.info(res)
        return res

class User(Resource):

    @property
    def AlreadyLogged(self):
        ticket = request.form.get("ticket", request.args.get("ticket"))
        if isLogged_in(ticket) in ("True", True):
            return True
        return False

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
        
        if getalluser:
            sql = "SELECT a.id, a.username, a.email, a.cname, a.avatar, a.motto, a.url, a.time, a.weibo, a.github, a.gender, a.extra, a.isAdmin FROM user_profile a"
            data = mysql.query(sql)
        elif getadminuser:
            sql  = "SELECT username FROM user_profile WHERE isAdmin=%s"
            data = mysql.query(sql, 'true')
            data = [ _["username"] for _ in data if _.get("username") ]
        elif username:
            sql = "SELECT a.id, a.username, a.email, a.cname, a.avatar, a.motto, a.url, a.time, a.weibo, a.github, a.gender, a.extra, a.isAdmin FROM user_profile a INNER JOIN user_oauth b ON a.username = b.oauth_username WHERE a.username=%s"
            data= mysql.get(sql, username)
            if not data:
                sql = "SELECT a.id, a.username, a.email, a.cname, a.avatar, a.motto, a.url, a.time, a.weibo, a.github, a.gender, a.extra, a.isAdmin FROM user_profile a INNER JOIN user_lauth b ON a.username = b.lauth_username WHERE a.username=%s"
                data = mysql.get(sql, username)
        else:
            sql, data = None, {}
        logger.info(sql)
        res.update(data=data)
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
        
        res      = {"code": 0, "success": False, "msg": None}
        data     = { k:v for k,v in request.form.iteritems() if k in ("email", "cname", "avatar", "motto", "url", "weibo", "github", "gender") }
        sql      = "UPDATE User SET "
        username = request.form.get("username")
        for k,v in data.iteritems():
            sql += "%s='%s'," %(k, v)
        sql = sql.strip(",") + " WHERE username=%s"
        logger.info("username: %s, sql: %s" %(username, sql))
        if username:
            try:
                mysql.update(sql, username)
            except Exception,e:
                logger.error(e, exc_info=True)
                success = False
            else:
                success = True
            res.update(success=success)
        logger.info(res)
        return res

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

api_blueprint = Blueprint(__name__, __name__)
api = Api(api_blueprint)
api.add_resource(Blog, '/blog', '/blog/', endpoint='blog')
api.add_resource(Misc, '/misc', '/misc/', endpoint='misc')
api.add_resource(User, '/user', '/user/', endpoint='user')
api.add_resource(Sys, '/sys', '/sys/', endpoint='sys')
