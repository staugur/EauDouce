# -*- coding: utf8 -*-

from flask import Blueprint, g, render_template
from utils.tool import admin_login_required, logger

admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/")
@admin_login_required
def index():
    return render_template("admin/index.html")

@admin_blueprint.route("/basic/blog/")
@admin_login_required
def basic_blog():
    return render_template("admin/basic/blog.html")

@admin_blueprint.route("/basic/user/")
@admin_login_required
def basic_user():
    return render_template("admin/basic/user.html")

@admin_blueprint.route("/basic/catalog/")
@admin_login_required
def basic_catalog():
    return render_template("admin/basic/catalog.html")

@admin_blueprint.route("/basic/commend/")
@admin_login_required
def basic_commend():
    return render_template("admin/basic/commend.html")

@admin_blueprint.route("/basic/project/")
@admin_login_required
def basic_project():
    return render_template("admin/basic/project.html")

@admin_blueprint.route("/basic/team/")
@admin_login_required
def basic_team():
    return render_template("admin/basic/team.html")

@admin_blueprint.route("/basic/filemanager/")
@admin_login_required
def basic_filemanager():
    return render_template("admin/basic/filemanager.html")

@admin_blueprint.route("/basic/plugin/")
@admin_login_required
def basic_plugin():
    return render_template("admin/basic/plugin.html")

@admin_blueprint.route("/system/configure/")
@admin_login_required
def system_config():
    return render_template("admin/system/configure.html")

@admin_blueprint.route("/system/notice/")
@admin_login_required
def system_notice():
    return render_template("admin/system/notice.html")

@admin_blueprint.route("/system/friendlink/")
@admin_login_required
def system_friendlink():
    return render_template("admin/system/friendlink.html")
