# -*- coding: utf-8 -*-
"""
    EauDouce.libs.api
    ~~~~~~~~~~~~~~

    Interface class.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import requests
from config import REDIS, MYSQL, PLUGINS
from torndb import IntegrityError, Connection
from utils.tool import api_logger, get_today, ListEqualSplit, md5
from .base import ServiceBase


class BlogApiManager(ServiceBase):


    def blog_search(self, q):
        "搜索文章标题"
        res    = {"msg": None, "data": [], "code": 0}
        sql    = "SELECT id,title,create_time,update_time,tag,author, FROM blog_article"
        data   = self.mysql_read.query(sql)
        res.update(data=[ blog for blog in data if q in blog["title"] ])
        api_logger.info(res)
        return res

    def blog_get_catalog_data(self, catalog, sort="desc", limit=None):
        "查询分类目录数据"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,catalog,author,create_time FROM blog_article WHERE catalog='%s' ORDER BY id %s %s" %(catalog, sort, LIMIT)
        api_logger.info("query catalog data SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="Catalog data query fail", code=100009)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res

    def blog_get_sources_data(self, sources, sort="desc", limit=None):
        "查询原创、转载、翻译文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        if sources:
            if sources == "1":
                sources = '原创'
            elif sources == "2":
                sources = '转载'
            elif sources == "3":
                sources = '翻译'
            #Original reproduced translation

            sql = "SELECT id,title,sources,author,create_time FROM blog_article WHERE sources='%s' ORDER BY id %s %s" %(sources, sort, LIMIT)
            api_logger.info("query sources data SQL: {}".format(sql))
            try:
                data = self.mysql_read.query(sql)
            except Exception,e:
                api_logger.error(e, exc_info=True)
                res.update(msg="Sources data query fail", code=100001)
            else:
                res.update(data=data)

        api_logger.info(res)
        return res

    def blog_get_tag_data(self, tag, sort="desc"):
        "查询某个tag的文章"

        res = {"msg": None, "data": [], "code": 0}
        sql = "SELECT id,title,tag,author,create_time FROM blog_article ORDER BY id {}".format(sort)
        api_logger.info("query tag data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="Tag data query fail", code=100004)
        else:
            tagData = []
            for _ in data:
                #if get_tags_data.decode('utf-8') in _.get('tag').split():
                if tag in _.get('tag').split():
                    tagData.append(_)
            res.update(data=tagData)

        api_logger.info(res)
        return res


    def blog_get_update_data(self, sort="desc", limit=None):
        "查询更新过的文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""      
        sql   = "SELECT id,title,create_time,update_time,tag FROM blog_article WHERE update_time IS NOT NULL ORDER BY update_time %s %s" %(sort, LIMIT)
        api_logger.info("query update_time data SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="query update data fail", code=100007)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res

    def blog_get_top_data(self, sort="desc", limit=None):
        "查询置顶文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,top FROM blog_article ORDER BY update_time %s %s" %(sort, LIMIT)
        api_logger.info("query top data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="Top data query fail", code=100003)
        else:
            res.update(data=[ _ for _ in data if _.get("top") in ("true", "True", True) ])

        api_logger.info(res)
        return res

    def blog_get_recommend_data(self, sort="desc", limit=None):
        "查询推荐文章"
        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,recommend FROM blog_article ORDER BY update_time %s %s" %(sort, LIMIT)
        api_logger.info("query recommend data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="Recommend data query fail", code=100002)
        else:
            res.update(data=[ _ for _ in data if _.get("recommend") in ("true", "True", True) ])

        api_logger.info(res)
        return res


    def blog_get_catalog_list(self):
        "获取分类目录列表"

        res = {"msg": None, "data": [], "code": 0}
        sql = 'SELECT catalog FROM blog_catalog'
        api_logger.info("query catalog list SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
            data = list(set([ v for _ in data for v in _.values() if v ]))
            #data = [ v.split(",")[0] for i in data for v in i.values() if v and v.split(",")[0] ]
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="query catalog data fail", code=100008)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res

    def blog_get_tags_list(self):
        "查询所有tag列表"

        res   = {"msg": None, "data": [], "code": 0}
        sql   = "SELECT tag FROM blog_article"
        api_logger.info("query tag list SQL: "+ sql)

        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="Tag list query fail", code=100005)
        else:
            tags = []
            for _ in data:
                if _.get('tag'):
                    tags += _.get("tag").split()
            data = list(set(tags))
            res.update(data=data)

        api_logger.info(res)
        return res


    def blog_get_single_index(self, sort="desc", limit=None, page=0, length=5):
        "获取所有文章简单数据索引"

        res   = {"msg": None, "data": [], "code": 0, "page": {}}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,tag,author,catalog FROM blog_article ORDER BY id %s %s" %(sort, LIMIT)
        api_logger.info("query single index SQL: %s" %sql)
        try:
            page = int(page)
            blog = self.mysql_read.query(sql)
            data = ListEqualSplit(blog, length)
            length = int(length)
            res.update(statistics=len(blog))
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="query single index fail", code=100006)
        else:
            if page < len(data):
                res.update(data=data[page], page={"page": page, "limit": limit, "length": length, "PageCount": len(data)})
            else:
                api_logger.info("get single index, but IndexOut with page "+page)

        api_logger.info(res)
        return res

    def blog_get_user_blog(self, user, sort="desc", limit=None):
        "查询某用户的博客"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,tag,catalog,sources,author from blog_article WHERE author='%s' ORDER BY id %s %s" %(user, sort, LIMIT)
        api_logger.info("query user blog SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update( msg="User blog data query fail", code=1000010)
        else:
            res.update(data=data)
        
        api_logger.info(res)
        return res


    def blog_get_id(self, blogId):
        "查询某个id的博客数据"

        res = {"msg": None, "data": [], "code": 0}
        sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author,recommend,top FROM blog_article WHERE id=%s" %blogId
        api_logger.info("get some id blog SQL: %s" %sql)
        try:
            data = self.mysql_read.get(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="get blog error", code=1000011)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res

    def blog_get_all(self, sort="desc", limit=None):
        "查询所有文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author,recommend,top FROM blog_article ORDER BY id %s %s" %(sort, LIMIT)
        api_logger.info("query all blog SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="get all blog error", code=1000012)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res


    def blog_create(self, **kwargs):
        "创建博客文章接口"

        res          = {"msg": None, "success": False, "code": 0}
        blog_title   = kwargs.get('title')
        blog_content = kwargs.get('content')
        blog_tag     = kwargs.get("tag")
        blog_catalog = kwargs.get("catalog", "未分类")
        blog_sources = kwargs.get("sources", "原创")
        blog_author  = kwargs.get("author", "admin")
        blog_ctime   = get_today()

        if blog_title and blog_content and blog_ctime and blog_author:
            sql = 'INSERT INTO blog_article (title,content,create_time,tag,catalog,sources,author) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            api_logger.info(sql %(blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author))
            try:
                blog_id  = self.mysql_write.insert(sql, blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author)
            except Exception,e:
                api_logger.error(e, exc_info=True)
                res.update(msg="Blog article failed to write, please try to resubmit.", code=1000013)
            else:
                res.update(msg="blog write success.", success=True, data=blog_id)
        else:
            res.update(msg="data in wrong format.", code=1000014)

        api_logger.info(res)
        return res

    def blog_update(self, **kwargs):
        "更新博客文章接口"

        res          = {"msg": None, "success": False, "code": 0}
        blog_title   = kwargs.get('title')
        blog_content = kwargs.get('content')
        blog_tag     = kwargs.get("tag")
        blog_catalog = kwargs.get("catalog", "未分类")
        blog_sources = kwargs.get("sources", "原创")
        blog_author  = kwargs.get("author", "admin")
        blog_blogId  = kwargs.get("blogId")
        blog_utime   = get_today()

        try:
            blog_blogId = int(blog_blogId)
        except ValueError,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="blogId form error.", code=1000015)
        else:
            if blog_title and blog_content and blog_utime and blog_author:
                sql = "UPDATE blog_article SET title=%s,content=%s,update_time=%s,tag=%s,catalog=%s,sources=%s,author=%s WHERE id=%s"
                try:
                    self.mysql_write.update(sql, blog_title, blog_content, blog_utime, blog_tag, blog_catalog, blog_sources, blog_author, blog_blogId)
                except Exception,e:
                    api_logger.error(e, exc_info=True)
                    res.update(msg="blog update error.", code=1000016)
                else:
                    res.update(success=True)
            else:
                res.update(msg="blog form error.", code=1000017)

        api_logger.info(res)
        return res

    def blog_delete(self, blogId):
        "删除文章"

        res = {"msg": None, "success": False, "code": 0}
        sql = "DELETE FROM blog_article WHERE id={}".format(blogId)
        api_logger.info("delete blog sql: "+sql)
        try:
            data = self.mysql_write.execute(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="delete blog error", code=1000018)
        else:
            res.update(success=True)

        api_logger.info(res)
        return res

    def blog_get_statistics(self):
        "统计数据查询"
        data = {
            "ArticleTotal": self.blog_get_single_index().get("statistics"),
            "CatalogTotal": len(self.blog_get_catalog_list().get("data")),
            "TagTotal": len(self.blog_get_tags_list().get("data")),
            "CommentTotal": None,
        }
        api_logger.info(data)
        return data

class MiscApiManager(ServiceBase):

    def misc_set_recommend(self, blogId, value="true"):
        """
        推荐或取消推荐文章: Recommended articles 
        #blogId: 文章ID;
        #value: 动作结果，true为推荐文章，false为取消推荐。
        """
        res = { "msg": None, "success": False, "code": 0}
        api_logger.info("blogId: %s, value: %s" %(blogId, value))

        #check params
        if not value in ("true", "True", True, "false", "False", False):
            res.update(msg="illegal parameter value", code=200001)
        try:
            blogId = int(blogId)
        except:
            res.update(msg="illegal parameter blogId", code=200002)
        if res['msg']:
            api_logger.info(res)
            return res

        try:
            #sql = "UPDATE blog_article SET update_time='%s',%s='%s' WHERE id=%d" %(get_today(), value, value, blogId)
            sql = "UPDATE blog_article SET recommend='{}' WHERE id={}".format(value, blogId)
            api_logger.info(sql)
            self.mysql_write.update(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="set or unset recommend error", success=False, code=200003)
        else:
            res.update(success=True)

        api_logger.info(res)
        return res

    def misc_set_top(self, blogId, value="true"):
        """
        置顶或取消置顶文章: Top articles 
        #blogId: 文章ID;
        #value: 动作结果，true为置顶文章，false为取消置顶。
        """
        res = {"msg": None, "success": False, "code": 0}
        api_logger.info("blogId: %s, value: %s" %(blogId, value))

        #check params
        if not value in ("true", "True", True, "false", "False", False):
            res.update(msg="illegal parameter value", code=200004)
        try:
            blogId = int(blogId)
        except:
            res.update(msg="illegal parameter blogId", code=200005)
        if res['msg']:
            api_logger.info(res)
            return res

        try:
            sql = "UPDATE blog_article SET top='{}' WHERE id={}".format(value, blogId)
            api_logger.info(sql)
            self.mysql_write.update(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(success=False, msg="set or unset top error", code=200006)
        else:
            res.update(success=True)

        api_logger.info(res)
        return res

    def misc_get_commend(self, blogId):
        """
        查询blogId的评论数
        """
        res = {"code": 0, "data": {}, "msg": None}

        if blogId:
            url = "http://changyan.sohu.com/api/2/topic/count?client_id={}&topic_source_id={}".format(PLUGINS['ChangyanComment']['appid'], blogId)
            try:
                data = requests.get(url).json().get("result").get(str(blogId))
            except Exception,e:
                api_logger.error(e, exc_info=True)
                res.update(msg="Comment Api Error", code=-1)
            else:
                res.update(data=data)
        else:
            res.update(msg="illegal parameter action", code=-1)

        api_logger.info(res)
        return res

    def misc_get_baiduincludedcheck(self, url):
        """查询收录URL情况"""

        res = {"code": 0, "msg": None, "Included": False}
        if "http://" in url or "https://" in url:
            result = BaiduIncludedCheck(url)
            res.update(Included=True)

        api_logger.info(res)
        return res

class UserApiManager(ServiceBase):

    @property
    def RegisteredUser(self):
        "返回本地已注册的用户名列表"

        sql = "SELECT lauth_username FROM user_lauth"
        api_logger.info("query registered user list SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            api_logger.warn("get user list error, return false")
            return False
        else:
            return [ _.get("lauth_username") for _ in data if _.get("lauth_username") ]

    def RegisteredUserInfo(self, username):
        "返回用户信息"

        sql = "SELECT lauth_username, lauth_password FROM user_lauth WHERE lauth_username=%s"
        api_logger.info("query user information SQL: {}".format(sql))

        try:
            data = self.mysql_read.get(sql, username)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            api_logger.warn("get user info error, return an empty dict")
            return {}
        else:
            return data

    @property
    def AlreadyLogged(self):
        ticket = request.form.get("ticket", request.args.get("ticket"))
        if isLogged_in(ticket) in ("True", True):
            return True
        return False

    def user_get_list(self, OAuth=False):
        "获取用户列表"

        res = {"code": 0, "msg": None, "data": []}
        sql = "SELECT lauth_username FROM user_lauth UNION SELECT oauth_username FROM user_oauth" if OAuth else "SELECT lauth_username FROM user_lauth"
        api_logger.info("get user list sql: "+ sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.info(e, exc_info=True)
            res.update(msg="get user list error", code=300001)
        else:
            res.update(data=[ _["lauth_username"] for _ in data if _.get("lauth_username") ])

        api_logger.info(res)
        return res

    def user_get_lauth_passwd(self, username):
        "获取本地用户密码"

        res = {"code": 0, "msg": None, "data": None}
        sql = "SELECT lauth_password FROM user_lauth WHERE lauth_username=%s"
        api_logger.info("get user password sql: "+ sql)
        try:
            data = self.mysql_read.get(sql, username)
        except Exception,e:
            api_logger.info(e, exc_info=True)
            res.update(msg="get user password error", code=300001)
        else:
            res.update(data=data.get("lauth_password"))

        api_logger.info(res)
        return res

    def user_get_all(self):
        "获取所有用户资料"

        res = {"code": 0, "msg": None, "data": []}
        sql = "SELECT a.id, a.username, a.email, a.cname, a.avatar, a.cover, a.motto, a.url, a.time, a.weibo, a.github, a.gender, a.extra, a.isAdmin, a.isAuthor FROM user_profile a"
        api_logger.info("get all user and profile sql: "+ sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.info(e, exc_info=True)
            res.update(msg="get all user error", code=300001)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res

    def user_get_one_profile(self, username):
        "查询用户资料"

        res = {"code": 0, "msg": None, "data": {}}        
        sql = "SELECT a.id, a.username, a.email, a.cname, a.avatar, a.cover, a.motto, a.url, a.time, a.weibo, a.github, a.gender, a.extra, a.isAdmin, a.isAuthor FROM user_profile a INNER JOIN user_oauth b ON a.username = b.oauth_username WHERE a.username=%s"
        data = self.mysql_read.get(sql, username)
        if not data:
            sql = "SELECT a.id, a.username, a.email, a.cname, a.avatar, a.cover, a.motto, a.url, a.time, a.weibo, a.github, a.gender, a.extra, a.isAdmin, a.isAuthor FROM user_profile a INNER JOIN user_lauth b ON a.username = b.lauth_username WHERE a.username=%s"
            data = self.mysql_read.get(sql, username)
        api_logger.info("get username profile sql: " + sql)
        res.update(data=data)
        api_logger.info(res)
        return res

    def user_get_admins(self):
        "获取管理员列表"
        res = {"code": 0, "msg": None, "data": []}
        sql = "SELECT username FROM user_profile WHERE isAdmin='true'"
        api_logger.info("query admin sql: " + sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="query admin account error", code=300001)
        else:
            res.update(data=[ _["username"] for _ in data if _.get("username") ])

        api_logger.info(res)
        return res

    def user_get_authors(self):
        "获取作者列表"
        res = {"code": 0, "msg": None, "data": []}
        sql = "SELECT username FROM user_profile WHERE isAuthor='true'"
        api_logger.info("query author sql: " + sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="query author account error", code=300002)
        else:
            res.update(data=[ _["username"] for _ in data if _.get("username") ])

        api_logger.info(res)
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
            api_logger.info(res)
            return res

        #check username and password length
        if 5 <= len(username) < 30 and 5 <= len(password) < 30:
            MD5password = md5(password)
        else:
            res.update({'msg': 'username or password length requirement is greater than or equal to 5 less than 30', 'code': 10002})
            api_logger.warn(res)
            return res

        #check username pattern
        if not user_pat.match(username):
            res.update({'msg': 'username is not valid', 'code': 10003})
            api_logger.warn(res)
            return res

        if email and mail_pat.match(email) == None:
            res.update({'msg': "email format error", 'code': 10004})
            api_logger.warn(res)
            return res

        #Start Action with (log, reg)
        if action == 'SignIn':
            api_logger.debug(RegisteredUser())
            api_logger.debug("MD5password: %s, DBpassword: %s, username: %s" %(MD5password, RegisteredUserInfo(username).get("lauth_password"),username))
            if username in RegisteredUser():
                if MD5password == RegisteredUserInfo(username).get("lauth_password"):
                    res.update({'msg': 'Password authentication success at sign in', 'code': 0, "success": True})
                else:
                    res.update({'msg': 'Password authentication failed at sign in', 'code': 10005, "success": False})
            else:
                res.update({'msg':'username not exists', 'code': 10006})
            api_logger.info(res)
            return res

        elif action == 'SignUp':
            try:
                AuthSQL = "INSERT INTO LAuth (lauth_username, lauth_password) VALUES(%s, %s)"
                api_logger.info(AuthSQL)
                mysql.insert(AuthSQL, username, MD5password)
                UserSQL = "INSERT INTO User (username, email, time, avatar) VALUES(%s, %s, %s, %s)"
                mysql.insert(UserSQL, username, email, get_today(), "/static/img/avatar/default.jpg")
            except IntegrityError, e:
                api_logger.error(e, exc_info=True)
                res.update({'msg': 'username already exists, cannot be registered!', 'code': 10007})
                api_logger.warn(res)
                return res
            except Exception,e:
                api_logger.error(e, exc_info=True)
                res.update(msg="server error", code=-1)
                api_logger.error(res)
                return res
            else:
                res.update({'code': 0, 'msg': 'Sign up success', "success": True})
                api_logger.info(res)
                return res

        else:
            res.update({'msg': 'Request action error', 'code': 10008})
            api_logger.info(res)
            return res

    def delete(self):
        #sql = "DELETE FROM user WHERE username=%s"
        #api_logger.info({"User:delete:SQL": sql})
        return {}

    def user_update_profile(self, username, **data):
        """Update user profile"""

        res  = {"code": 0, "success": False, "msg": None}
        #data = { k:v for k,v in kwargs.iteritems() if k in ("email", "cname", "avatar", "motto", "url", "weibo", "github", "gender") }
        sql  = "UPDATE user_profile SET "
        for k,v in data.iteritems():
            sql += "%s='%s'," %(k, v)
        sql = sql.strip(",") + " WHERE username=%s"
        api_logger.info("username: %s, sql: %s" %(username, sql))
        if username:
            try:
                self.mysql_write.update(sql, username)
            except Exception,e:
                api_logger.error(e, exc_info=True)
                success = False
            else:
                success = True
            res.update(success=success)
        api_logger.info(res)
        return res

    def user_update_avatar(self, username, avatarUrl):
        """Update user avatar"""
        
        res = {"code": 0, "success": False, "msg": None}
        sql = "UPDATE user_profile SET avatar=%s WHERE username=%s"
        if username:
            try:
                self.mysql_write.update(sql, avatarUrl, username)
            except Exception,e:
                api_logger.error(e, exc_info=True)
            else:
                res.update(success=True)

        api_logger.info(res)
        return res

    def user_update_cover(self, username, coverUrl):
        """Update user cover"""
        
        res = {"code": 0, "success": False, "msg": None}
        sql = "UPDATE user_profile SET cover=%s WHERE username=%s"
        if username:
            try:
                self.mysql_write.update(sql, coverUrl, username)
            except Exception,e:
                api_logger.error(e, exc_info=True)
            else:
                res.update(success=True)

        api_logger.info(res)
        return res

    def user_update_password(self, username, OldPassword, NewPassword):
        """Update user password"""
        
        res = {"code": 0, "success": False, "msg": None}

        if username in self.user_get_list().get("data", []) and md5(OldPassword) == self.user_get_lauth_passwd(username).get("data"):
            sql = "UPDATE user_lauth SET lauth_password=%s WHERE lauth_username=%s"
            if 5 <= len(NewPassword) < 30:
                try:
                    self.mysql_write.update(sql, md5(NewPassword), username)
                except Exception,e:
                    api_logger.error(e, exc_info=True)
                else:
                    res.update(success=True)
            else:
                res.update(msg='password length requirement is greater than or equal to 5 less than 30', code= 300002)
        else:
            res.update(msg="username does not exist or old passwords do not match", code=300002)

        api_logger.info(res)
        return res

    def user_get_statistics(self):
        "统计数据查询"
        pass

class SysApiManager(ServiceBase):

    def get_sys_notice(self):
        "查询系统公告数据"

        res = {"code": 0, "msg": None, "data": None}

        sql = "SELECT msg FROM sys_notice"
        api_logger.info("query notice data with sql: " + sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e)
            res.update(msg="query notice data error", code=400001)
        else:
            res.update(data=[ _.get("msg") for _ in data if _.get("msg") ])

        api_logger.info(res)
        return res

    def get_sys_config(self):
        "查询系统配置"

        res = {"code": 0, "msg": None, "data": None}
        sql = "SELECT * FROM sys_config"
        api_logger.info("query config data with sql: " + sql)
        try:
            data = self.mysql_read.get(sql)
        except Exception,e:
            api_logger.error(e)
            res.update(msg="query config data error", code=400002)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res

    def get_sys_friendlink(self):
        "查询系统中的友链"

        res = {"code": 0, "msg": None, "data": None}
        sql = "SELECT id,link,title FROM sys_friendlink"
        api_logger.info("query friend link data with sql: " + sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            api_logger.error(e)
            res.update(msg="query friend link data error", code=400003)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res

    def ClickMysqlWrite(self, data):
        if isinstance(data, dict):
            if data.get("ip") and data.get("agent") and data.get("method") in ("GET", "POST", "PUT", "DELETE", "OPTIONS"):
                try:
                    Ipd = requests.get("http://ip.taobao.com/service/getIpInfo.php?ip={}".format(data.get("ip")), timeout=5, headers={"Use-Agent": data.get("agent")}).json().get("data", {})
                except Exception,e:
                    api_logger.debug(e)
                    Ipd = {}
                sql = "insert into blog_clicklog set url=%s, ip=%s, agent=%s, method=%s, status_code=%s, referer=%s, isp=%s"
                try:
                    self.mysql_write.insert(sql, data.get("url"), data.get("ip"), data.get("agent"), data.get("method"), data.get("status_code"), data.get("referer"), "{} {} {} {} {}".format(Ipd.get("country"), Ipd.get("area"), Ipd.get("region"), Ipd.get("city"), Ipd.get("isp")))
                except Exception, e:
                    api_logger.warn(e, exc_info=True)
        else:
            api_logger.debug("Do not record this log")

    def post_apply_author(self, username):
        """
        申请成为作者
        #username(str): 用户名
        """

        res = {"msg": None, "code": 0}
        if username and username in self.user_get_list(True).get("data"):
            if username in self.user_get_authors().get("data"):
                res.update(msg="The current user is the author")
            else:
                sql = "INSERT INTO blog_applyauthor (username, req_time) VALUES(%s, %s)"
                try:
                    mid = self.mysql_write.insert(sql, username, get_today())
                except IntegrityError,e:
                    api_logger.debug(e)
                    res.update(msg="The author has applied.", code=400006)
                except Exception,e:
                    api_logger.error(e, exc_info=True)
                    res.update(msg="server error", code=400004)
                else:
                    res.update(success=True, data=mid)
        else:
            res.update(msg="No author username", code=400005)

        api_logger.info(res)
        return res

    def get_apply_author(self, isActive=1):
        """
        查询有效的作者申请
        #isActive(int), 查询是否有效的申请, 0无效, 1有效
        """

        res = {"code": 0, "msg": None, "data": None}
        sql = "SELECT id,username,req_time FROM blog_applyauthor WHERE isActive=%s AND req_state='wait'"
        try:
            data = self.mysql_read.query(sql, isActive)
        except Exception,e:
            api_logger.error(e, exc_info=True)
            res.update(msg="server error", code=400007)
        else:
            res.update(data=data)

        api_logger.info(res)
        return res

class ApiManager(BlogApiManager, MiscApiManager, UserApiManager, SysApiManager):
    pass
