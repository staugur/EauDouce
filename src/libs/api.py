# -*- coding: utf-8 -*-
"""
    EauDouce.libs.api
    ~~~~~~~~~~~~~~

    Interface class.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import requests, sys, json
from config import PLUGINS
from torndb import IntegrityError
from utils.tool import logger, get_today, ListEqualSplit, md5, DO, user_pat, sql_safestring_check
from .base import ServiceBase


class BlogApiManager(ServiceBase):

    def get_banner(self):
        res = dict(msg=None)
        data = [
            {'imgUrl':'https://img.saintic.com/interest.blog/blog/9045593365244993.png','title':'来：订阅更新本站吆！','id':200, "isActive": False},
            {'imgUrl':'https://img.saintic.com/interest.blog/blog/201701032126317486.png','title':'Python抓取花瓣网画板图片','id':204, "isActive": False},
            {'imgUrl':'https://img.saintic.com/interest.blog/blog/swarm.png','title':'开源项目之SwarmOps','id':217, "isActive": True},
        ]
        res.update(data=data)
        return res
    
    def get_source_html(self):
        sql  = "SELECT id,title,content FROM blog_article"
        return self.mysql_read.query(sql)

    def blog_search(self, q):
        "搜索文章标题"
        reload(sys)
        sys.setdefaultencoding('utf-8')
        #q = unicode(q)
        res = {"msg": None, "data": [], "code": 0}
        logger.api.debug("blog_search query: {0}, query type: {1}".format(q, type(q)))
        if ";" in q:
            res.update(msg="Parameter is not legal", code=-1)
        else:
            sql  = "SELECT id,title,create_time,update_time,tag,author FROM blog_article WHERE title LIKE '%%{0}%%' OR content LIKE '%%{0}%%';".format(q)
            data = self.mysql_read.query(sql)
            #res.update(data=[ blog for blog in data if q in blog["title"] ])
            res.update(data=data)
            logger.api.info(sql)
        logger.api.debug(res)
        return res

    def blog_get_catalog_data(self, catalog, sort="desc", limit=None):
        "查询分类目录数据"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,catalog,author,create_time FROM blog_article WHERE catalog='%s' ORDER BY id %s %s" %(catalog, sort, LIMIT)
        logger.api.info("query catalog data SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Catalog data query fail", code=100009)
        else:
            res.update(data=data)

        logger.api.debug(res)
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
            logger.api.info("query sources data SQL: {}".format(sql))
            try:
                data = self.mysql_read.query(sql)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="Sources data query fail", code=100001)
            else:
                res.update(data=data)

        logger.api.debug(res)
        return res

    def blog_get_tag_data(self, tag, sort="desc"):
        "查询某个tag的文章"

        res = {"msg": None, "data": [], "code": 0}
        sql = "SELECT id,title,tag,author,create_time FROM blog_article ORDER BY id {}".format(sort)
        logger.api.info("query tag data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Tag data query fail", code=100004)
        else:
            tagData = []
            for _ in data:
                #if get_tags_data.decode('utf-8') in _.get('tag').split():
                if tag in _.get('tag').split():
                    tagData.append(_)
            res.update(data=tagData)

        logger.api.debug(res)
        return res


    def blog_get_update_data(self, sort="desc", limit=None):
        "查询更新过的文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""      
        sql   = "SELECT id,title,create_time,update_time,tag FROM blog_article WHERE update_time IS NOT NULL ORDER BY update_time %s %s" %(sort, LIMIT)
        logger.api.info("query update_time data SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="query update data fail", code=100007)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def blog_get_top_data(self, sort="desc", limit=None):
        "查询置顶文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,top FROM blog_article ORDER BY update_time %s %s" %(sort, LIMIT)
        logger.api.info("query top data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Top data query fail", code=100003)
        else:
            res.update(data=[ _ for _ in data if _.get("top") in ("true", "True", True) ])

        logger.api.debug(res)
        return res

    def blog_get_recommend_data(self, sort="desc", limit=None):
        "查询推荐文章"
        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,recommend FROM blog_article ORDER BY update_time %s %s" %(sort, LIMIT)
        logger.api.info("query recommend data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Recommend data query fail", code=100002)
        else:
            res.update(data=[ _ for _ in data if _.get("recommend") in ("true", "True", True) ])

        logger.api.debug(res)
        return res


    def blog_get_catalog_list(self):
        "获取分类目录列表"

        res = {"msg": None, "data": [], "code": 0}
        sql = 'SELECT catalog FROM blog_catalog'
        logger.api.info("query catalog list SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
            data = list(set([ v for _ in data for v in _.values() if v ]))
            #data = [ v.split(",")[0] for i in data for v in i.values() if v and v.split(",")[0] ]
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="query catalog data fail", code=100008)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def blog_get_tags_list(self):
        "查询所有tag列表"

        res   = {"msg": None, "data": [], "code": 0}
        sql   = "SELECT tag FROM blog_article"
        logger.api.info("query tag list SQL: "+ sql)

        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Tag list query fail", code=100005)
        else:
            tags = []
            for _ in data:
                if _.get('tag'):
                    tags += _.get("tag").split()
            data = list(set(tags))
            res.update(data=data)

        logger.api.debug(res)
        return res


    def blog_get_single_index(self, sort="desc", limit=None, page=0, length=5):
        "获取所有文章简单数据索引"

        res   = {"msg": None, "data": [], "code": 0, "page": {}}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,tag,author,catalog FROM blog_article ORDER BY id %s %s" %(sort, LIMIT)
        logger.api.info("query single index SQL: %s" %sql)
        try:
            page = int(page)
            blog = self.mysql_read.query(sql)
            data = ListEqualSplit(blog, length)
            length = int(length)
            res.update(statistics=len(blog))
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="query single index fail", code=100006)
        else:
            if page < len(data):
                res.update(data=data[page], page={"page": page, "limit": limit, "length": length, "PageCount": len(data)})
            else:
                logger.api.info("get single index, but IndexOut with page {}".format(page))

        logger.api.debug(res)
        return res

    def blog_get_user_blog(self, user, sort="desc", limit=None):
        "查询某用户的博客 user=uid"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,tag,catalog,sources,author from blog_article WHERE author='%s' ORDER BY id %s %s" %(user, sort, LIMIT)
        logger.api.info("query user blog SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update( msg="User blog data query fail", code=1000010)
        else:
            res.update(data=data)
        
        logger.api.debug(res)
        return res

    def blog_refresh_id_cache(self, blogId):
        """刷新某个id博客数据缓存"""
        key = "EauDouce:blog:{}:cache".format(blogId)
        kid = self.redis.delete(key)
        return True if isinstance(kid, (int, long)) else False

    def blog_get_id(self, blogId):
        "查询某个id的博客数据"

        res = {"msg": None, "data": [], "code": 0}
        key = "EauDouce:blog:{}:cache".format(blogId)
        if self.redis.exists(key):
            data = json.loads(self.redis.get(key))
            res.update(data=data)
            logger.api.info("hit blog cache")
        else:
            sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author,recommend,top FROM blog_article WHERE id=%s" %blogId
            try:
                data = self.mysql_read.get(sql)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="get blog error", code=1000011)
            else:
                res.update(data=data)
                self.redis.set(key, json.dumps(data))
                self.redis.expire(key, 600)

        logger.api.debug(res)
        return res

    def blog_get_all(self, limit=None, sort="desc"):
        "查询所有文章"

        res = {"msg": None, "data": [], "code": 0}
        sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author,recommend,top FROM blog_article ORDER BY id %s %s" %(sort, "LIMIT %s" %limit if limit else "")
        logger.api.info("query all blog SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="get all blog error", code=1000012)
        else:
            res.update(data=data)

        logger.api.debug(res)
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
            logger.api.info(sql %(blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author))
            try:
                blog_id  = self.mysql_write.insert(sql, blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="Blog article failed to write, please try to resubmit.", code=1000013)
            else:
                res.update(msg="blog write success.", success=True, data=blog_id)
        else:
            res.update(msg="data in wrong format.", code=1000014)

        logger.api.debug(res)
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
            logger.api.error(e, exc_info=True)
            res.update(msg="blogId form error.", code=1000015)
        else:
            if blog_title and blog_content and blog_utime and blog_author:
                sql = "UPDATE blog_article SET title=%s,content=%s,update_time=%s,tag=%s,catalog=%s,sources=%s,author=%s WHERE id=%s"
                try:
                    self.mysql_write.update(sql, blog_title, blog_content, blog_utime, blog_tag, blog_catalog, blog_sources, blog_author, blog_blogId)
                except Exception,e:
                    logger.api.error(e, exc_info=True)
                    res.update(msg="blog update error.", code=1000016)
                else:
                    res.update(success=True, msg=self.blog_refresh_id_cache(blog_blogId))
            else:
                res.update(msg="blog form error.", code=1000017)

        logger.api.debug(res)
        return res

    def blog_delete(self, blogId):
        "删除文章"

        res = {"msg": None, "success": False, "code": 0}
        sql = "DELETE FROM blog_article WHERE id={}".format(blogId)
        logger.api.info("delete blog sql: "+sql)
        try:
            data = self.mysql_write.execute(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="delete blog error", code=1000018)
        else:
            res.update(success=True, msg=self.blog_refresh_id_cache(blogId))

        logger.api.debug(res)
        return res

    def blog_get_statistics(self):
        "统计数据查询"
        data = {
            "ArticleTotal": self.blog_get_single_index().get("statistics"),
            "CatalogTotal": len(self.blog_get_catalog_list().get("data")),
            "TagTotal": len(self.blog_get_tags_list().get("data")),
            "CommentTotal": None,
        }
        logger.api.info(data)
        return data

class MiscApiManager(ServiceBase):

    def misc_set_recommend(self, blogId, value="true"):
        """
        推荐或取消推荐文章: Recommended articles 
        #blogId: 文章ID;
        #value: 动作结果，true为推荐文章，false为取消推荐。
        """
        res = { "msg": None, "success": False, "code": 0}
        logger.api.info("blogId: %s, value: %s" %(blogId, value))

        #check params
        if not value in ("true", "True", True, "false", "False", False):
            res.update(msg="illegal parameter value", code=200001)
        try:
            blogId = int(blogId)
        except:
            res.update(msg="illegal parameter blogId", code=200002)
        if res['msg']:
            logger.api.debug(res)
            return res

        try:
            #sql = "UPDATE blog_article SET update_time='%s',%s='%s' WHERE id=%d" %(get_today(), value, value, blogId)
            sql = "UPDATE blog_article SET recommend='{}' WHERE id={}".format(value, blogId)
            logger.api.info(sql)
            self.mysql_write.update(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="set or unset recommend error", success=False, code=200003)
        else:
            res.update(success=True, msg=self.blog_refresh_id_cache(blogId))

        logger.api.debug(res)
        return res

    def misc_set_top(self, blogId, value="true"):
        """
        置顶或取消置顶文章: Top articles 
        #blogId: 文章ID;
        #value: 动作结果，true为置顶文章，false为取消置顶。
        """
        res = {"msg": None, "success": False, "code": 0}
        logger.api.info("blogId: %s, value: %s" %(blogId, value))

        #check params
        if not value in ("true", "True", True, "false", "False", False):
            res.update(msg="illegal parameter value", code=200004)
        try:
            blogId = int(blogId)
        except:
            res.update(msg="illegal parameter blogId", code=200005)
        if res['msg']:
            logger.api.debug(res)
            return res

        try:
            sql = "UPDATE blog_article SET top='{}' WHERE id={}".format(value, blogId)
            logger.api.info(sql)
            self.mysql_write.update(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(success=False, msg="set or unset top error", code=200006)
        else:
            res.update(success=True, msg=self.blog_refresh_id_cache(blogId))

        logger.api.debug(res)
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
                logger.api.error(e, exc_info=True)
                res.update(msg="Comment Api Error", code=-1)
            else:
                res.update(data=data)
        else:
            res.update(msg="illegal parameter action", code=-1)

        logger.api.debug(res)
        return res

    def misc_get_baiduincludedcheck(self, url):
        """查询收录URL情况"""

        res = {"code": 0, "msg": None, "Included": False}
        if "http://" in url or "https://" in url:
            result = BaiduIncludedCheck(url)
            res.update(Included=True)

        logger.api.debug(res)
        return res

    def misc_BaiduActivePush(self, pushUrl, original=True):
        """百度主动推送(实时)接口提交链接，每个链接3次提交机会，超过后不允许提交
        @param pushUrl str: 提交的链接
        @param original bool: 是否原创
        """
        res = dict(msg=None, success=False)
        key = "EauDouce:BaiduActivePushUrls:hash"
        callUrl = PLUGINS['BaiduActivePush']['callUrl']
        callUrl = callUrl + "&type=original" if original else callUrl
        pushTimes = int(self.redis.hget(key, pushUrl) or 0)
        logger.api.debug("pushUrl: {}, original: {}, pushTimes: {}, check: {}".format(pushUrl, original, pushTimes, 0 <= pushTimes <= 3))
        if 0 <= pushTimes <= 3:
            try:
                data = requests.post(url=callUrl, data=pushUrl, timeout=3, headers={"User-Agent": "BaiduActivePush/www.saintic.com"}).json()
            except Exception,e:
                logger.api.warning(e, exc_info=True)
                res.update(msg="push failed")
            else:
                # data like {u'success_realtime': 0, u'remain_realtime': 0}
                logger.api.info("BaiduActivePush PushUrl is %s, Result is %s" % (pushUrl, data))
                if int(data.get("success_realtime") or data.get("success") or 0) == 1:
                    res.update(success=True)
                    self.redis.hincrby(key, pushUrl, 1)
        else:
            res.update(msg="No submission authority", success=True)
        return res

class UserApiManager(ServiceBase):


    def sso_get_userinfo(self, uid):
        key = "EauDouce:userinfo:{}".format(uid)
        if uid:
            try:
                data = json.loads(self.redis.get(key))
            except Exception,e:
                logger.sys.debug(e)
            else:
                return data
        return dict()

    def sso_set_userinfo(self, uid, userinfo, expire=None):
        key = "EauDouce:userinfo:{}".format(uid)
        if uid and userinfo and isinstance(userinfo, dict):
            source = self.sso_get_userinfo(uid)
            source.update(userinfo)
            try:
                self.redis.set(key, json.dumps(source))
                if isinstance(expire, int):
                    self.redis.expire(key, expire)
            except Exception,e:
                logger.sys.debug(e)
            else:
                return True
        return False

    def user_get_list(self, OAuth=False):
        "获取用户列表, OAuth: 没用"
        sql = "SELECT uid FROM user_profile"
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            return []
        else:
            return [ _.get("uid") for _ in data if _.get("uid") ]


    def user_get_all(self):
        "获取所有用户资料"
        res = {"code": 0, "msg": None, "data": []}
        sql = "SELECT * FROM user_profile"
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="get all user error", code=300001)
        else:
            res.update(data=data)
        return res

    def user_get_one_profile(self, username):
        "返回用户信息, username = uid"
        sql = "SELECT * FROM user_profile WHERE uid=%s"
        res = dict(data=dict(), msg=None)
        try:
            data = self.mysql_read.get(sql, username)
        except Exception,e:
            logger.api.error(e, exc_info=True)
        else:
            res.update(data=data)
        return res

    def user_get_admins(self):
        "获取管理员列表"
        res = {"code": 0, "msg": None, "data": []}
        sql = "SELECT uid FROM user_profile WHERE is_admin=1"
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="query admin account error", code=300001)
        else:
            res.update(data=[ _["uid"] for _ in data if _.get("uid") ])
        return res

    def user_get_authors(self):
        "获取作者列表"
        admins = self.user_get_admins()["data"]
        authors = []
        return dict(code=0, msg=None, data=admins + authors)

    def user_update_cover(self, username, coverUrl):
        """Update user cover"""
        res = {"code": 0, "success": False, "msg": None}
        return res

    def user_get_domainName(self, uid):
        """根据uid获取域名"""
        res = dict(code=1, msg=None)
        if uid:
            sql = "SELECT domain_name FROM user_profile WHERE uid=%s"
            try:
                data = self.mysql_read.get(sql, uid)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="get domain_name error", code=2)
            else:
                if data and isinstance(data, dict) and data["domain_name"]:
                    res.update(domain_name=data["domain_name"], code=0)
                else:
                    res.update(code=404)
        else:
            res.update(msg="Invaild uid", code=3)
        logger.api.debug(res)
        return res

    def user_getprofile_with_domainName(self, domainName):
        """根据个性域名地址获取个人资料"""
        res = {"code": 1, "msg": None}
        sql = "SELECT * FROM user_profile WHERE domain_name=%s"
        if domainName and user_pat.match(domainName) and sql_safestring_check(domainName):
            try:
                data = self.mysql_read.get(sql, domainName)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="get user error", code=300009)
            else:
                if data and isinstance(data, dict):
                    res.update(data=data, code=0)
                else:
                    res.update(code=404)
        else:
            res.update(msg="Invaild domain_name", code=1)
        logger.api.debug(res)
        return res

class SysApiManager(ServiceBase):

    def get_sys_notice(self):
        "查询系统公告数据"

        res = {"code": 0, "msg": None, "data": None}

        sql = "SELECT id,msg FROM sys_notice"
        logger.api.info("query notice data with sql: " + sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e)
            res.update(msg="query notice data error", code=400001)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def post_sys_notice(self, noticeMsg):
        "添加系统公告"

        res = {"code": 0, "msg": None, "success": False}
        sql = "INSERT INTO sys_notice (msg) VALUES (%s)"
        if not noticeMsg:
            res.update(msg="msg is empty")
        else:
            try:
                data = self.mysql_write.insert(sql, noticeMsg)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="post a notice data error", code=400002)
            else:
                res.update(data=data, success=True)

        logger.api.debug(res)
        return res

    def delete_sys_notice(self, noticeId):
        """删除系统公告"""
        res = {"code": 0, "msg": None, "success": False}
        sql = "DELETE FROM sys_notice WHERE id=%d" %int(noticeId)
        try:
            self.mysql_write.execute(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
        else:
            res.update(success=True)
        logger.api.debug(res)
        return res

    def get_sys_config(self):
        "查询系统配置"

        res = {"code": 0, "msg": None, "data": None}
        sql = "SELECT * FROM sys_config"
        logger.api.info("query config data with sql: " + sql)
        try:
            data = self.mysql_read.get(sql)
        except Exception,e:
            logger.api.error(e)
            res.update(msg="query config data error", code=400002)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def get_sys_friendlink(self):
        "查询系统中的友链"

        res = {"code": 0, "msg": None, "data": None}
        sql = "SELECT id,link,title FROM sys_friendlink"
        logger.api.info("query friend link data with sql: " + sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e)
            res.update(msg="query friend link data error", code=400003)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def post_sys_friendlink(self, link, title):
        "添加友情链接"

        res = {"code": 0, "msg": None, "success": False}
        sql = "INSERT INTO sys_friendlink (link,title) VALUES (%s,%s)"
        if not link or not title:
            res.update(msg="param error")
        else:
            try:
                data = self.mysql_write.insert(sql, link, title)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="post a friendlink data error", code=400005)
            else:
                res.update(success=True)

        logger.api.debug(res)
        return res

    def delete_sys_friendlink(self, friendlinkId):
        """删除友情链接"""
        res = {"code": 0, "msg": None, "success": False}
        sql = "DELETE FROM sys_friendlink WHERE id=%d" %int(friendlinkId)
        try:
            self.mysql_write.execute(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
        else:
            res.update(success=True)
        logger.api.debug(res)
        return res

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
                    logger.api.debug(e)
                    res.update(msg="The author has applied.", code=400006)
                except Exception,e:
                    logger.api.error(e, exc_info=True)
                    res.update(msg="server error", code=400004)
                else:
                    res.update(success=True, data=mid)
        else:
            res.update(msg="No author username", code=400005)

        logger.api.debug(res)
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
            logger.api.error(e, exc_info=True)
            res.update(msg="server error", code=400007)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def update_sys_configure(self, **kwargs):
        """更新配置"""

        data= DO(kwargs)
        res = {"code": 0, "msg": None, "success": False}
        sql = "UPDATE sys_config SET about_awi=%s, about_ww=%s, about_address=%s, about_phone=%s, about_email=%s, about_beian=%s, seo_keywords=%s, seo_description=%s, site_title=%s, site_feedname=%s,applet=%s"
        try:
            data = self.mysql_write.update(sql, data.about_awi, data.about_ww, data.about_address, data.about_phone, data.about_email, data.about_beian, data.seo_keywords, data.seo_description, data.site_title, data.site_feedname, data.applet)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="update configure data error")
        else:
            res.update(success=True)

        logger.api.debug(res)
        return res

    def post_applet_users(self, **kwargs):
        """记录微信小程序访问用户"""
        data = dict(
            avatarUrl=kwargs.get("avatarUrl"),
            country=kwargs.get("country"),
            province=kwargs.get("province"),
            city=kwargs.get("city"),
            gender=kwargs.get("gender"),
            nickName=kwargs.get("nickName")
        )
        res = dict(success=False, msg=None)
        key = "EauDouce:AppletUsers"
        if data:
            rid = self.redis.sadd(key, json.dumps(data))
            if rid == 1:
                res.update(success=True)
            else:
                res.update(msg="Not added. May already exist.")
        else:
            res.update(msg="param error")
        logger.api.debug(res)
        return res

    def get_applet_users(self):
        """查询微信小程序访问用户"""
        res = dict(data=[], msg=None)
        key = "EauDouce:AppletUsers"
        data = self.redis.smembers(key)
        if isinstance(data, set):
            data = list(data)
        res.update(data=[json.loads(i) for i in data if i])
        return res

    def sys_get_clicklog(self):
        sql = "SELECT id,url,agent,method,ip,status_code,referer,isp,browserType,browserDevice,browserOs,browserFamily FROM blog_clicklog ORDER BY id DESC LIMIT 100"
        return self.mysql_read.query(sql)

class ApiManager(BlogApiManager, MiscApiManager, UserApiManager, SysApiManager):
    pass
