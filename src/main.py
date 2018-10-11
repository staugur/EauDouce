# -*- coding: utf-8 -*-
"""
    EauDouce.main
    ~~~~~~~~~~~~~~

    This is a blog program based on Flask:
    This is an entry files, main applications, and some initialization operations.

    Docstring conventions:
    http://flask.pocoo.org/docs/0.10/styleguide/#docstrings

    Comments:
    http://flask.pocoo.org/docs/0.10/styleguide/#comments

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

__author__  = "Mr.tao"
__email__   = "staugur@saintic.com"
__doc__     = "A flask+mysql+bootstrap blog based on personal interests and hobbies."
__date__    = "2017-03-26"
__version__ = "0.0.1"
__license__ = "MIT"

import time, os.path, jinja2, sys, rq_dashboard
from flask import request, g, render_template, redirect, make_response, url_for
from flask_pluginkit import PluginManager, blueprint, Flask
from config import GLOBAL, SSO, PLUGINS, REDIS
from utils.tool import logger, ChoiceColor, TagRandomColor, timestamp_to_timestring
from utils.web import verify_sessionId, analysis_sessionId, get_redirect_url
from urllib import urlencode
from libs.api import ApiManager
from views import api_blueprint, front_blueprint, admin_blueprint, upload_blueprint
reload(sys)
sys.setdefaultencoding('utf-8')

#初始化定义application
app = Flask(__name__)
app.config.update(
    REDIS_URL = REDIS,
    RQ_POLL_INTERVAL = 2500,
    PLUGINKIT_AUTHMETHOD = "BOOL",
    PLUGINKIT_GUNICORN_ENABLED = True,
    PLUGINKIT_GUNICORN_PROCESSNAME = 'gunicorn: master [%s]' %GLOBAL['ProcessName']
)

#初始化插件管理器(自动扫描并加载运行)
plugin = PluginManager(app, logger=logger.plugin, stpl=True)

#初始化接口管理器
api = ApiManager()

#注册蓝图路由,可以修改前缀
app.register_blueprint(front_blueprint)
app.register_blueprint(api_blueprint, url_prefix="/api")
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(upload_blueprint, url_prefix="/upload")
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rqdashboard")
app.register_blueprint(blueprint, url_prefix="/PluginManager")

@app.context_processor  
def GlobalTemplateVariables():  
    data = {"Version": __version__, "Author": __author__, "Email": __email__, "Doc": __doc__, "ChoiceColor": ChoiceColor, "TagRandomColor": TagRandomColor, "timestamp_to_timestring": timestamp_to_timestring, "PLUGINS": PLUGINS}
    return data

@app.before_request_top
def before_request():
    g.startTime = time.time()
    g.signin    = verify_sessionId(request.cookies.get("sessionId"))
    g.sid,g.uid = analysis_sessionId(request.cookies.get("sessionId"), "tuple") if g.signin else (None, None)
    g.username  = g.uid
    g.api       = api
    g.plugins   = PLUGINS
    g.userinfo  = api.sso_get_userinfo(g.uid)
    # 仅是重定向页面快捷定义
    g.redirect_uri = get_redirect_url()
    logger.access.debug("sid: {}, uid: {}, userinfo: {}".format(g.sid, g.uid, g.userinfo))

@app.after_request
def after_request(response):
    data = {
        "status_code": response.status_code,
        "method": request.method,
        "ip": request.headers.get('X-Real-Ip', request.remote_addr),
        "url": request.url,
        "referer": request.headers.get('Referer'),
        "agent": request.headers.get("User-Agent"),
        "TimeInterval": "%0.2fs" %float(time.time() - g.startTime)
    }
    logger.access.info(data)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.errorhandler(404)
def not_found(error=None):
    return render_template('public/404.html'),404

@app.errorhandler(500)
def server_error(error=None):
    if error:
        logger.err.error(error, exc_info=True)
    return render_template('public/500.html'),500

@app.route('/login/')
def login():
    if g.signin:
        return redirect(url_for("front.index"))
    else:
        ReturnUrl = request.args.get("NextUrl") or request.args.get("ReturnUrl")
        SSOLoginURL = url_for("sso.Login", ReturnUrl=ReturnUrl) if ReturnUrl else url_for("sso.Login")
        return redirect(SSOLoginURL) 

@app.route('/logout/')
def logout():
    # 注销
    if g.signin:
        return redirect(url_for("sso.Logout"))
    else:
        return redirect(url_for("sso.Login"))

@app.route('/SignUp')
def signup():
    regUrl = SSO.get("sso_server").strip("/") + "/signUp"
    return redirect(regUrl)

if __name__ == '__main__':
    app.run(host=GLOBAL.get('Host'), port=int(GLOBAL.get('Port')), debug=True)
