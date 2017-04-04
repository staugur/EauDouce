# -*- coding: utf8 -*-

import requests, datetime, SpliceURL
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from flask import Blueprint, g, render_template, request, redirect, url_for, make_response, abort
#from config import SSO, PLUGINS, BLOG
#from utils.public import logger, md5, BaiduActivePush
#from libs import get_blogId_data, get_user_profile, get_user_blog, get_index_list, get_index_data

front_blueprint = Blueprint("front", __name__, template_folder="templates", static_folder='static')

data = [{
         "author": "admin",
         "catalog": "Interest.blog",
         "content": u"           <p></p><p>           </p><h2><p><b>我是干什么的？</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">SA，DevOpser</code></pre><p><b>这个站点为什么存在？</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">记录技术点滴，开源项目源码，分享经验与技术。</code></pre><p><b>本站历程：</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">Interest.blog之前，\r\n--&gt;最初的PHP(wordpress、emlog等)\r\n--&gt;GitHub Page\r\n--&gt;Python Flask(saintic/blog-&gt;saintic/Team/Front-&gt;Interest.blog)\r\n如果你有好的文章、想法、经验想与大家分享，或者文章有错误，请及时告诉我，欢迎投稿。</code></pre><p><b>如何联系我？</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">如果还有问题想联系我？比如协同开发项目、谈谈人生聊聊理想啊，OK，我的邮箱是：staugur@saintic.com\r\n或者查看页脚部分的“邮我”按钮，给我们团队发邮件：<span style=\"font-size: 0.8em; color: rgb(17, 17, 17); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;\">developers@saintic.com。</span></code></pre></h2><h2><p><b>Public：</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">我的GitHub组织代码仓库是--&gt;&gt; https:<span class=\"hljs-regexp\">//gi</span>thub.com/saintic\r\n\r\n我的GitHub私人代码仓库是--&gt;&gt; https:<span class=\"hljs-regexp\">//gi</span>thub.com/staugur\r\n\r\n我的Docker仓库名是staugur--&gt;&gt; docker search staugur\r\n\r\n订阅本站最近更新的文章--&gt;&gt; <a href=\"http://www.saintic.com/blog/200.html\" target=\"_blank\" style=\"font-size: 0.8em; font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;\">http://www.saintic.com/blog/200.html</a></code></pre><p>另外如果你想砸死我，可以扫描下面的二维码试试：\r\n</p></h2><h2><img src=\"http://img.saintic.com/interest.blog/blog/5226820977404714.png\" alt=\"22-24-34-alipay\" class=\"\" style=\"font-size: 16px;\"><br></h2>",
         "create_time": "2016-11-05",
         "id": 113,
         "sources": u"原创",
         "tag": "Interest.blog",
         "title": u"关于我们",
         "update_time": "2016-12-08"
      },
      {
         "author": "taochengwei",
         "catalog": "python",
         "content": u"           <p></p><p>           </p><h2><p><b>我是干什么的？</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">SA，DevOpser</code></pre><p><b>这个站点为什么存在？</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">记录技术点滴，开源项目源码，分享经验与技术。</code></pre><p><b>本站历程：</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">Interest.blog之前，\r\n--&gt;最初的PHP(wordpress、emlog等)\r\n--&gt;GitHub Page\r\n--&gt;Python Flask(saintic/blog-&gt;saintic/Team/Front-&gt;Interest.blog)\r\n如果你有好的文章、想法、经验想与大家分享，或者文章有错误，请及时告诉我，欢迎投稿。</code></pre><p><b>如何联系我？</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">如果还有问题想联系我？比如协同开发项目、谈谈人生聊聊理想啊，OK，我的邮箱是：staugur@saintic.com\r\n或者查看页脚部分的“邮我”按钮，给我们团队发邮件：<span style=\"font-size: 0.8em; color: rgb(17, 17, 17); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;\">developers@saintic.com。</span></code></pre></h2><h2><p><b>Public：</b></p><pre style=\"max-width: 100%;\"><code class=\"coffeescript hljs\" codemark=\"1\">我的GitHub组织代码仓库是--&gt;&gt; https:<span class=\"hljs-regexp\">//gi</span>thub.com/saintic\r\n\r\n我的GitHub私人代码仓库是--&gt;&gt; https:<span class=\"hljs-regexp\">//gi</span>thub.com/staugur\r\n\r\n我的Docker仓库名是staugur--&gt;&gt; docker search staugur\r\n\r\n订阅本站最近更新的文章--&gt;&gt; <a href=\"http://www.saintic.com/blog/200.html\" target=\"_blank\" style=\"font-size: 0.8em; font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;\">http://www.saintic.com/blog/200.html</a></code></pre><p>另外如果你想砸死我，可以扫描下面的二维码试试：\r\n</p></h2><h2><img src=\"http://img.saintic.com/interest.blog/blog/5226820977404714.png\" alt=\"22-24-34-alipay\" class=\"\" style=\"font-size: 16px;\"><br></h2>",
         "create_time": "2016-11-05",
         "id": 114,
         "sources": u"原创",
         "tag": "python",
         "title": u"这是一篇测试文章",
         "update_time": "2016-12-08"
      }]

@front_blueprint.route("/")
def index():
    return render_template("index.html", blogData=data)

'''
@front_page.route('/blog/<int:bid>.html')
def blogShow(bid):
    data = get_blogId_data(bid)
    if data:
        if PLUGINS['BaiduActivePush']['enable'] in ("true", "True", True):
            original = True if data.get("sources") == "原创" else False
            BaiduActivePush(request.url, original=original)
        return render_template("front/blogShow.html", blogId=bid, data=data)
    else:
        return abort(404)

@front_page.route("/blog/edit/")
def blogEdit():
    blogId = request.args.get("blogId")
    if g.signin and blogId:
        data = get_blogId_data(blogId)
        if data and g.username == data.get("author") or g.username in g.admins:
            return render_template("front/blogEdit.html", blogId=blogId, data=data)
    return redirect(url_for(".login"))

@front_page.route("/blog/write/")
def blogWrite():
    if g.signin:
        return render_template("front/blogWrite.html")
    else:
        return redirect(url_for(".login"))

@front_page.route("/blog/resources/")
def blogResources():
    return render_template("front/resources.html")

@front_page.route("/home/")
@front_page.route("/home/<user>/")
def home(user=None):
    logger.debug(user)
    if g.signin:
        user = get_user_profile(g.username)
        blog = get_user_blog(g.username)
        return render_template("front/home.html", user=user, blog=blog)
    else:
        return redirect(url_for(".login"))

@front_page.route("/user/profile/")
def profile():
    if g.signin:
        user = get_user_profile(g.username)
        return render_template("front/profile.html", user=user)
    else:
        return redirect(url_for(".login"))

@front_page.route("/user/UpdatePasswd", methods=["POST",])
def UpdatePasswd():
    if g.signin:
        logger.debug(request.form)
        #ImmutableMultiDict([('username', u'admin'), ('new_pass', u''), ('new_repass', u''), ('old_pass', u'')])
    else:
        abort(403)

@front_page.route('/login/')
def login():
    if g.signin:
        return redirect(url_for(".index"))
    else:
        query = {"sso": True,
           "sso_r": SpliceURL.Modify(request.url_root, "/sso/").geturl,
           "sso_p": SSO["SSO.PROJECT"],
           "sso_t": md5("%s:%s" %(SSO["SSO.PROJECT"], SpliceURL.Modify(request.url_root, "/sso/").geturl))
        }
        SSOLoginURL = SpliceURL.Modify(url=SSO["SSO.URL"], path="/login/", query=query).geturl
        logger.info("User request login to SSO: %s" %SSOLoginURL)
        return redirect(SSOLoginURL)

@front_page.route('/logout/')
def logout():
    SSOLogoutURL = SSO.get("SSO.URL") + "/sso/?nextUrl=" + request.url_root.strip("/")
    resp = make_response(redirect(SSOLogoutURL))
    resp.set_cookie(key='logged_in', value='', expires=0)
    resp.set_cookie(key='username',  value='', expires=0)
    resp.set_cookie(key='sessionId',  value='', expires=0)
    resp.set_cookie(key='time',  value='', expires=0)
    resp.set_cookie(key='Azone',  value='', expires=0)
    return resp

@front_page.route('/sso/')
def sso():
    ticket = request.args.get("ticket")
    logger.info("ticket: %s" %ticket)
    username, expires, sessionId = ticket.split('.')
    if expires == 'None':
        UnixExpires = None
    else:
        UnixExpires = datetime.datetime.strptime(expires,"%Y-%m-%d")
    resp = make_response(redirect(url_for(".index")))
    #resp.set_cookie(key="test", value="ok", expires=datetime.datetime.strptime(expires,"%Y-%m-%d"))
    #resp.set_cookie(key='test', value="ok", max_age=ISOString2Time(expires))
    resp.set_cookie(key='logged_in', value="yes", expires=UnixExpires)
    resp.set_cookie(key='username',  value=username, expires=UnixExpires)
    resp.set_cookie(key='sessionId', value=sessionId, expires=UnixExpires)
    resp.set_cookie(key='time', value=expires, expires=UnixExpires)
    resp.set_cookie(key='Azone', value="sso", expires=UnixExpires)
    return resp

@front_page.route("/google32fd52b6c900160b.html")
def google_search_console():
    return render_template("public/google32fd52b6c900160b.html")

@front_page.route("/robots.txt")
def robots():
    return """
User-agent: *
Disallow: 
Sitemap: http://www.saintic.com/sitemap.xml
    """

@front_page.route("/sitemap.xml")
def sitemap():
    resp = make_response(render_template("public/sitemap.xml", data=get_index_list()))
    resp.headers["Content-Type"] = "application/xml"    
    return resp

@front_page.route("/feed")
@front_page.route("/feed/")
def feed():
    data = get_index_data(limit=10)
    logger.debug(data)
    feed = AtomFeed('Interest.blog Feed', feed_url=request.url, url=request.url_root, subtitle="From the latest article in www.saintic.com")
    for article in data:
        feed.add(article['title'], unicode(article['content']),
                 content_type='html',
                 author=article['author'],
                 id=article['id'],
                 url=urljoin(request.url_root, url_for(".blogShow", bid=article['id'])),
                 updated=datetime.datetime.strptime(article['update_time'] or article['create_time'],"%Y-%m-%d"),
                 published=datetime.datetime.strptime(article['create_time'],"%Y-%m-%d"))
    return feed.get_response()

@front_page.route("/webscan_360_cn.html")
def webscan_360_cn():
    return render_template("public/webscan_360_cn.html")

@front_page.route("/openSource/")
def openSource():
    return render_template("front/openSource.html")
'''