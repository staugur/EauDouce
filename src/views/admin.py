# -*- coding: utf8 -*-

from flask import Blueprint, g, render_template
from utils.tool import admin_login_required, logger


admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/")
@admin_login_required
def index():
    return render_template("admin/index.html")

@admin_blueprint.route("/blogManager/")
@admin_login_required
def blog():
    return render_template("admin/blog.html")

@admin_blueprint.route("/systemConf/")
@admin_login_required
def system():
    return render_template("admin/system.html")

