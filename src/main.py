# -*- coding: utf8 -*-

import json, datetime, SpliceURL, time
from flask import Flask, request, g, jsonify, redirect, make_response, url_for
from config import GLOBAL, SSO
from utils.tool import logger, isLogged_in, md5, login_required
from urllib import urlencode
from libs.api import ApiManager
from views.front import front_blueprint
#from views.api import api_blueprint

__author__  = 'Mr.tao'
__email__   = 'staugur@saintic.com'
__doc__     = 'A flask+mysql+bootstrap blog based on personal interests and hobbies.'
__date__    = '2017-03-26'
__org__     = 'SaintIC'
__version__ = '0.0.1'

app = Flask(__name__)
api = ApiManager()
app.register_blueprint(front_blueprint, url_prefix="/blog")
#app.register_blueprint(api_blueprint, url_prefix="/api")

@app.before_request
def before_request():
    g.startTime = time.time()
    g.sessionId = request.cookies.get("sessionId", "")
    g.username  = request.cookies.get("username", "")
    g.expires   = request.cookies.get("time", "")
    g.signin    = isLogged_in('.'.join([ g.username, g.expires, g.sessionId ]))
    g.sysInfo   = {"Version": __version__, "Author": __author__, "Email": __email__, "Doc": __doc__}
    g.api       = api
    app.logger.info(app.url_map)
    app.logger.debug(dir(g.api))

@app.after_request
def after_request(response):
    logger.info(json.dumps({
        "AccessLog": {
            "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            "TimeInterval": "%0.2fs" %float(time.time() - g.startTime)
            }
        }
    ))
    return response

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'code': 404,
        'msg': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/')
def index():
    return redirect(url_for("front.index"))

@app.route('/login/')
def login():
    if g.signin:
        return redirect(url_for("index"))
    else:
        query = {"sso": True,
           "sso_r": SpliceURL.Modify(request.url_root, "/sso/").geturl,
           "sso_p": SSO["SSO.PROJECT"],
           "sso_t": md5("%s:%s" %(SSO["SSO.PROJECT"], SpliceURL.Modify(request.url_root, "/sso/").geturl))
        }
        SSOLoginURL = SpliceURL.Modify(url=SSO["SSO.URL"], path="/login/", query=query).geturl
        logger.info("User request login to SSO: %s" %SSOLoginURL)
        return redirect(SSOLoginURL)

@app.route('/logout/')
def logout():
    SSOLogoutURL = SSO.get("SSO.URL") + "/sso/?nextUrl=" + request.url_root.strip("/")
    resp = make_response(redirect(SSOLogoutURL))
    resp.set_cookie(key='logged_in', value='', expires=0)
    resp.set_cookie(key='username',  value='', expires=0)
    resp.set_cookie(key='sessionId',  value='', expires=0)
    resp.set_cookie(key='time',  value='', expires=0)
    resp.set_cookie(key='Azone',  value='', expires=0)
    return resp

@app.route('/sso/')
def sso():
    ticket = request.args.get("ticket")
    logger.info("ticket: %s" %ticket)
    username, expires, sessionId = ticket.split('.')
    if expires == 'None':
        UnixExpires = None
    else:
        UnixExpires = datetime.datetime.strptime(expires,"%Y-%m-%d")
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie(key='logged_in', value="yes", expires=UnixExpires)
    resp.set_cookie(key='username',  value=username, expires=UnixExpires)
    resp.set_cookie(key='sessionId', value=sessionId, expires=UnixExpires)
    resp.set_cookie(key='time', value=expires, expires=UnixExpires)
    resp.set_cookie(key='Azone', value="sso", expires=UnixExpires)
    return resp

@app.route('/SignUp')
def signup():
    return redirect(SSO.get("SSO.URL").strip("/") + "/SignUp")

if __name__ == '__main__':
    Host  = GLOBAL.get('Host')
    Port  = GLOBAL.get('Port')
    app.run(host = Host, port = int(Port), debug = True)
