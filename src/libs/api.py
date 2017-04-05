# -*- coding: utf8 -*-

from config import MYSQL
from torndb import IntegrityError, Connection
from utils.tool import logger, ParseMySQL

RegisteredUser = lambda :[ _.get("lauth_username") for _ in mysql.query("SELECT lauth_username FROM user_lauth") if _.get("lauth_username") ]
RegisteredUserInfo = lambda username:mysql.get("SELECT lauth_username, lauth_password FROM user_lauth WHERE lauth_username=%s", username)

class ApiManager(object):

    def __init__(self):
        self.mysql = Connection(
                    host     = "%s:%s" %(ParseMySQL(MYSQL).get('Host'), ParseMySQL(MYSQL).get('Port', 3306)),
                    database = ParseMySQL(MYSQL).get('Database'),
                    user     = ParseMySQL(MYSQL).get('User'),
                    password = ParseMySQL(MYSQL).get('Password'),
                    time_zone= ParseMySQL(MYSQL).get('Timezone','+8:00'),
                    charset  = ParseMySQL(MYSQL).get('Charset', 'utf8'),
                    connect_timeout=3,
                    max_idle_time=2)

    def get_sources_data(self, sources, sort="desc", limit=None):
        "查询原创、转载、翻译文章"
        res   = {"msg": None, "data": [], "code": -0}
        LIMIT = "LIMIT " + str(limit) if limit else ""

        if sources:
            if sources == "1":
                sources = '原创'
            elif sources == "2":
                sources = '转载'
            elif sources == "3":
                sources = '翻译'
            #Original reproduced translation

            sql = "SELECT id,title,sources FROM blog_article WHERE sources='%s' ORDER BY id %s %s" %(sources, sort, LIMIT)
            logger.info("query sources data SQL: {}".format(sql))
            try:
                data = self.mysql.query(sql)
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(msg="Sources data query fail", code=1000.1)
            else:
                res.update(data=data)

        logger.info(res)
        return res

    def get_recommend_data(self, sort="desc", limit=None):
        "查询推荐文章"
        res   = {"msg": None, "data": [], "code": -0}
        LIMIT = "LIMIT " + str(limit) if limit else ""

        sql = "SELECT id,title,create_time,update_time,recommend FROM blog_article ORDER BY update_time %s %s" %(sort, LIMIT)
        logger.info("query recommend data SQL: {}".format(sql))
        try:
            data = self.mysql.query(sql)
        except Exception,e:
            logger.error(e, exc_info=True)
            res.update(msg="Recommend data query fail", code=1000.2)
        else:
            res.update(data=[ _ for _ in data if _.get("recommend") in ("true", "True", True) ])

        logger.info(res)
        return res

    def get_top_data(self, sort="desc", limit=None):
        "查询置顶文章"
        res   = {"msg": None, "data": [], "code": -0}
        LIMIT = "LIMIT " + str(limit) if limit else ""

        sql = "SELECT id,title,create_time,update_time,top FROM blog_article ORDER BY update_time %s %s" %(sort, LIMIT)
        logger.info("query top data SQL: {}".format(sql))
        try:
            data = self.mysql.query(sql)
        except Exception,e:
            logger.error(e, exc_info=True)
            res.update(msg="Top data query fail", code=1000.3)
        else:
            res.update(data=[ _ for _ in data if _.get("top") in ("true", "True", True) ])

        logger.info(res)
        return res

    def get_tag_data(self, tag, sort="desc"):
        "查询某个tag的文章"
        res   = {"msg": None, "data": [], "code": -0}

        sql = "SELECT id,title,tag FROM blog_article ORDER BY id {}".format(sort)
        logger.info("query tag data SQL: {}".format(sql))
        try:
            data = self.mysql.query(sql)
        except Exception,e:
            logger.error(e, exc_info=True)
            res.update(msg="Tag data query fail", code=1000.4)
        else:
            tagData = []
            for _ in data:
                #if get_tags_data.decode('utf-8') in _.get('tag').split():
                if tag in _.get('tag').split():
                    tagData.append(_)
            res.update(data=tagData)

        logger.info(res)
        return res

'''
        if get_tags_list:
            sql  = "SELECT tag FROM blog_article"
            data = mysql.query(sql)
            tags = []
            for _ in data:
                if _.get('tag'):
                    logger.debug(_.get("tag").split())
                    tags += _.get("tag").split()
            res.update(data=list(set(tags)))
            logger.info(res)
            return res

        if get_index_only:
            sql = "SELECT id,title,create_time,update_time,tag FROM blog_article ORDER BY id %s %s" %(sort, LIMIT)
            logger.info("SELECT title only SQL: %s" %sql)
            try:
                data = mysql.query(sql)
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(data=[], msg="Only title query fail", code=7)
            else:
                res.update(data=data)
            logger.info(res)
            return res

        if get_update_data:
            sql = "SELECT id,title,create_time,update_time,tag FROM blog_article WHERE update_time IS NOT NULL ORDER BY update_time %s %s" %(sort, LIMIT)
            logger.info("SELECT update_time data SQL: %s" %sql)
            try:
                data = mysql.query(sql)
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(data=[], msg="Update data query fail", code=8)
            else:
                res.update(data=data)
            logger.info(res)
            return res

        if get_catalog_list:
            #sql = "SELECT GROUP_CONCAT(catalog) FROM blog GROUP BY catalog"
            sql = 'SELECT catalog FROM blog_article'
            logger.info("SELECT catalog list SQL: %s" %sql)
            try:
                data = mysql.query(sql)
                logger.info(data)
                data = list(set([ v for _ in data for v in _.values() if v ]))
                #data = [ v.split(",")[0] for i in data for v in i.values() if v and v.split(",")[0] ]
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(data=[], msg="Catalog query fail", code=1)
            else:
                res.update(data=data)
            logger.info(res)
            return res

        if get_sources_list:
            #sql = "SELECT GROUP_CONCAT(sources) FROM blog GROUP BY sources"
            sql = 'SELECT sources FROM blog_article'
            logger.info("SELECT sources list SQL: %s" %sql)
            try:
                data = mysql.query(sql)
                logger.info(data)
                #data = [ v.split(",")[0] for i in data for v in i.values() if v and v.split(",")[0] ]
                data = list(set([ v for _ in data for v in _.values() if v ]))
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(data=[], msg="Sources query fail", code=2)
            else:
                res.update(data=data)
            logger.info(res)
            return res

        if get_catalog_data:
            #sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author FROM blog WHERE catalog='%s' ORDER BY id %s %s" %(get_catalog_data, sort, LIMIT)
            sql = "SELECT id,title,catalog FROM blog_article WHERE catalog='%s' ORDER BY id %s %s" %(get_catalog_data, sort, LIMIT)
            logger.info("SELECT catalog data SQL: %s" %sql)
            try:
                data = mysql.query(sql)
                logger.info(data)
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(data=[], msg="Catalog data query fail", code=3)
            else:
                res.update(data=data)
            logger.info(res)
            return res


        if get_user_blog:
            sql = "SELECT id,title,create_time,tag,catalog,sources,author from blog_article WHERE author='%s' ORDER BY id %s %s" %(get_user_blog, sort, LIMIT)
            logger.info("SELECT user blog SQL: %s" %sql)
            try:
                data = mysql.query(sql)
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(data=[], msg="User blog data query fail", code=7)
            else:
                res.update(data=data)
            logger.info(res)
            return res


        if blogId:
            sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author,recommend,top FROM blog_article WHERE id=%s" %blogId
            #sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author FROM blog ORDER BY id %s %s" %(sort, LIMIT)
            logger.info({"Blog:get:SQL": sql})
            try:
                data = mysql.get(sql)
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(msg="get blog error", code=6)
            else:
                res.update(data=data)

        elif num:
            sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author FROM blog_article ORDER BY id %s %s" %(sort, LIMIT)
            logger.info({"Blog:get:SQL": sql})
            try:
                data = mysql.query(sql)
            except Exception,e:
                logger.error(e, exc_info=True)
                res.update(msg="get all blog error", code=6)
            else:
                res.update(data=data)

        logger.info(res)
        return res

    def post(self):
        """ 创建博客文章接口 """
        #get blog form informations.
        blog_title   = request.form.get('title')
        blog_content = request.form.get('content')
        blog_ctime   = get_today()
        blog_tag     = request.form.get("tag")
        blog_catalog = request.form.get("catalog", "linux")
        blog_sources = request.form.get("sources", "原创")
        blog_author  = request.form.get("author")
        logger.info("blog_title:%s, blog_content:%s, blog_ctime:%s, blog_tag:%s, blog_catalog:%s, blog_sources:%s, blog_author:%s" %(blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author))
        if blog_title and blog_content and blog_ctime and blog_author:
            sql = 'INSERT INTO blog_article (title,content,create_time,tag,catalog,sources,author) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            logger.info(sql %(blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author))
            try:
                blog_id  = mysql.insert(sql, blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author)
            except Exception,e:
                logger.error(e, exc_info=True)
                res = {"code": 3, "data": None, "msg": "blog write error."}
            else:
                res = {"code": 0, "data": blog_id, "msg": "blog write success."}
        else:
            res = {"code": 4, "data": None, "msg": "data form error."}
        logger.info(res)
        return res

    def put(self):
        """ 更新博客文章接口 """
        blog_title   = request.form.get('title')
        blog_content = request.form.get('content')
        blog_utime   = get_today()
        blog_tag     = request.form.get("tag")
        blog_catalog = request.form.get("catalog", "linux")
        blog_sources = request.form.get("sources", "原创")
        blog_author  = request.form.get("author")
        blog_blogId  = request.form.get("blogId")
        logger.info("Update blog, blog_title:%s, blog_content:%s, blog_utime:%s, blog_tag:%s, blog_catalog:%s, blog_sources:%s, blog_author:%s, blog_blogId:%s" %(blog_title, blog_content, blog_utime, blog_tag, blog_catalog, blog_sources, blog_author, blog_blogId))
        try:
            blog_blogId = int(blog_blogId)
        except ValueError,e:
            logger.error(e, exc_info=True)
            res = {"code": 5, "msg": "blog form error."}
        else:
            if blog_title and blog_content and blog_utime and blog_author:
                sql = "UPDATE blog SET title=%s,content=%s,update_time=%s,tag=%s,catalog=%s,sources=%s,author=%s WHERE id=%s"
                try:
                    mysql.update(sql, blog_title, blog_content, blog_utime, blog_tag, blog_catalog, blog_sources, blog_author, blog_blogId)
                except Exception,e:
                    logger.error(e, exc_info=True)
                    res = {"code": 6, "msg": "blog write error."}
                else:
                    res = {"code": 0, "success": True, "msg": None}
            else:
                res = {"code": 7, "success": False, "msg": "blog form error."}
        logger.info(res)
        return res
'''

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

