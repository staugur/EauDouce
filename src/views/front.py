# -*- coding: utf8 -*-

import requests, datetime, SpliceURL
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from flask import Blueprint, g, render_template, request, redirect, url_for, make_response, abort
from utils.tool import login_required,logger


front_blueprint = Blueprint("front", __name__)

@front_blueprint.route("/")
def index():
    return render_template("front/index.html")

@front_blueprint.route('/<int:bid>.html')
def blogShow(bid):
    data = g.api.blog_get_id(bid).get("data")
    if data:
        return render_template("front/blogShow.html", blogId=bid, data=data)
    else:
        return abort(404)

@login_required
@front_blueprint.route("/write/")
def blogWrite():
    return render_template("front/blogWrite.html")

@front_blueprint.route("/edit/")
def blogEdit():
    blogId = request.args.get("blogId")
    if g.signin and blogId:
        data = g.api.blog_get_id(blogId).get("data")
        logger.error(data)
        if data:
            if g.username == data.get("author") or g.username in g.api.user_get_admins().get("data"):
                return render_template("front/blogEdit.html", blogId=blogId, data=data)
        return abort(404)
    return redirect(url_for("login"))
###
@front_blueprint.route("/home/")
@front_blueprint.route("/home/<user>/")
def home(user=None):
    logger.debug(user)
    if g.signin:
        user = get_user_profile(g.username)
        blog = get_user_blog(g.username)
        return render_template("front/home.html", user=user, blog=blog)
    else:
        return redirect(url_for(".login"))

@front_blueprint.route("/user/profile/")
def profile():
    if g.signin:
        user = get_user_profile(g.username)
        return render_template("front/profile.html", user=user)
    else:
        return redirect(url_for(".login"))

@front_blueprint.route("/user/UpdatePasswd", methods=["POST",])
def UpdatePasswd():
    if g.signin:
        logger.debug(request.form)
        #ImmutableMultiDict([('username', u'admin'), ('new_pass', u''), ('new_repass', u''), ('old_pass', u'')])
    else:
        abort(403)

@front_blueprint.route("/google32fd52b6c900160b.html")
def google_search_console():
    return render_template("public/google32fd52b6c900160b.html")

@front_blueprint.route("/robots.txt")
def robots():
    return """
User-agent: *
Disallow: 
Sitemap: http://www.saintic.com/sitemap.xml
    """

@front_blueprint.route("/sitemap.xml")
def sitemap():
    resp = make_response(render_template("public/sitemap.xml", data=get_index_list()))
    resp.headers["Content-Type"] = "application/xml"    
    return resp

@front_blueprint.route("/feed")
@front_blueprint.route("/feed/")
def feed():
    data = g.api.blog_get_all(limit=10).get("data")
    feed = AtomFeed(u'清水蓝天博客源', feed_url=request.url, url=request.url_root, subtitle="From the latest article in EauDouce")
    for article in data:
        updated = article['update_time'][:10] if article['update_time'] else article['create_time'][:10]
        feed.add(article['title'], unicode(article['content']),
                 content_type='html',
                 author=article['author'],
                 id=article['id'],
                 url=urljoin(request.url_root, url_for(".blogShow", bid=article['id'])),
                 updated=datetime.datetime.strptime(updated, "%Y-%m-%d"),
                 published=datetime.datetime.strptime(article['create_time'][:10], "%Y-%m-%d"))
    return feed.get_response()
