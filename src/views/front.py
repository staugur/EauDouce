# -*- coding: utf-8 -*-
"""
    EauDouce.views.front
    ~~~~~~~~~~~~~~

    Foreground view.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import datetime
from werkzeug.contrib.atom import AtomFeed
from flask import Blueprint, g, render_template, request, redirect, url_for, make_response, abort
from utils.tool import logger
from utils.web import login_required
from config import SSO

front_blueprint = Blueprint("front", __name__)

@front_blueprint.route("/")
def index():
    return render_template("front/blogIndex.html")

@front_blueprint.route('/blog/<int:bid>.html')
def blogShow(bid):
    data = g.api.blog_get_id(bid).get("data")
    if data:
        return render_template("front/blogShow.html", blogId=bid, data=data, original=True if data.get("sources") == "原创" else False)
    else:
        return abort(404)

@front_blueprint.route("/blog/write/")
@login_required
def blogWrite():
    return render_template("front/blogWrite.html")

@front_blueprint.route("/blog/edit/")
@login_required
def blogEdit():
    blogId = request.args.get("blogId")
    if blogId:
        data = g.api.blog_get_id(blogId).get("data")
        if data:
            if g.username == data.get("author") or g.username in g.api.user_get_admins().get("data"):
                return render_template("front/blogEdit.html", blogId=blogId, data=data)
        return abort(404)

@front_blueprint.route("/blog/resource/")
def blogResource():
    return render_template("front/blogResource.html")

@front_blueprint.route("/blog/search/")
def blogSearch():
    return render_template("front/blogSearch.html")

@front_blueprint.route("/user/go/")
def userGo():
    # 过渡性的路由，用于使用uid跳转到userIndex的情况
    uid = request.args.get("uid") or g.uid
    res = g.api.user_get_domainName(uid)
    if res["code"] == 0:
        return redirect(url_for("front.userIndex", domain_name=res["domain_name"]))
    else:
        return abort(404)

@front_blueprint.route("/user/<domain_name>")
def userIndex(domain_name):
    # 用户主页
    res = g.api.user_getprofile_with_domainName(domain_name)
    if res["code"] == 0:
        return render_template("front/userIndex.html", userdata=res["data"], blogdata=g.api.blog_get_user_blog(res["data"]["uid"])["data"])
    else:
        return abort(404)

@front_blueprint.route("/user/setting/")
@login_required
def userSet():
    return redirect("{}/user/setting/".format(SSO["sso_server"].strip("/")))

@front_blueprint.route("/user/ChangeAvater/")
@login_required
def userChangeAvater():
    return redirect("{}/user/setting/#avatar".format(SSO["sso_server"].strip("/")))
    return render_template("front/userChangeAvater2.html")
    return render_template("front/userChangeAvater.html")

@front_blueprint.route("/user/ChangePassword/")
@login_required
def userChangePassword():
    return redirect("{}/user/setting/#pass".format(SSO["sso_server"].strip("/")))
    return render_template("front/userChangePassword.html")

@front_blueprint.route("/user/ChangeCover/")
@login_required
def userChangeCover():
    return u"暂不开放"
    return render_template("front/userChangeCover.html")

@front_blueprint.route("/user/ChangeProfile/")
@login_required
def userChangeProfile():
    return redirect("{}/user/setting/".format(SSO["sso_server"].strip("/")))
    return render_template("front/userChangeProfile.html")

@front_blueprint.route("/robots.txt")
def robots():
    return """
User-agent: *
Disallow: 
    """

@front_blueprint.route("/sitemap.xml")
def sitemapxml():
    resp = make_response(render_template("public/sitemap.xml"))
    resp.headers["Content-Type"] = "application/xml"    
    return resp

@front_blueprint.route("/sitemap.html")
def sitemaphtml():
    # 站点地图
    return render_template("public/sitemap.html")

@front_blueprint.route("/BingSiteAuth.xml")
def BingSiteAuth():
    # Bing验证
    return render_template("public/BingSiteAuth.xml")

@front_blueprint.route("/feed/")
def feed():
    # 订阅
    data = g.api.blog_get_all(limit=10).get("data")
    feed = AtomFeed(g.api.get_sys_config().get("data").get("site_feedname"), feed_url=request.url, url=request.url_root, subtitle="From the latest article in {}".format(request.url))
    for article in data:
        updated = article['update_time'][:10] if article['update_time'] else article['create_time'][:10]
        feed.add(article['title'], unicode(article['content']),
                 content_type='html',
                 author=article['author'],
                 id=article['id'],
                 url=url_for(".blogShow", bid=article['id'], utm_source='feed', _external=True),
                 updated=datetime.datetime.strptime(updated, "%Y-%m-%d"),
                 published=datetime.datetime.strptime(article['create_time'][:10], "%Y-%m-%d"))
    return feed.get_response()

@front_blueprint.route("/thirds/StaticUpload/")
def thirdPluginStaticUpload():
    return render_template("admin/thirdPluginStaticUpload.html")
