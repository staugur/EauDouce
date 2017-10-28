# -*- coding: utf-8 -*-
"""
    EauDouce.utils.tool
    ~~~~~~~~~~~~~~

    Common function.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import re, requests, hashlib, datetime, random, upyun
from uuid import uuid4
from log import Logger
from base64 import b32encode
from config import SSO, PLUGINS
from functools import wraps
from threading import Thread
from flask import g, request, redirect, url_for

class DO(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

ip_pat          = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
mail_pat        = re.compile(r"([0-9a-zA-Z\_*\.*\-*]+)@([a-zA-Z0-9\-*\_*\.*]+)\.([a-zA-Z]+$)")
user_pat        = re.compile(r'[a-zA-Z\_][0-9a-zA-Z\_]')
comma_pat       = re.compile(r"\s*,\s*")
logger          = DO(
                    sys = Logger("sys").getLogger,
                    sso = Logger("sso").getLogger,
                    api = Logger("api").getLogger,
                    access = Logger("access").getLogger,
                    plugin = Logger("plugin").getLogger
                  )
md5             = lambda pwd:hashlib.md5(pwd).hexdigest()
gen_token       = lambda n=32:b32encode(uuid4().hex)[:n]
gen_requestId   = lambda :str(uuid4())
get_today       = lambda format="%Y-%m-%d %H:%M":datetime.datetime.now().strftime(format)
gen_rnd_filename= lambda :"%s%s" %(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randrange(1000, 10000)))
ListEqualSplit  = lambda l,n=5: [ l[i:i+n] for i in range(0,len(l), n) ]


def ip_check(ip):
    if isinstance(ip, (str, unicode)):
        return ip_pat.match(ip)

def isLogged_in(cookie_str):
    ''' check username is logged in '''

    SSOURL = SSO.get("SSO.URL")
    if cookie_str and not cookie_str == '..':
        username, expires, sessionId = cookie_str.split('.')
        try:
            success = requests.post(SSOURL+"/sso/", data={"username": username, "time": expires, "sessionId": sessionId}, timeout=3, verify=False, headers={"User-Agent": "SSO.Client"}).json().get("success", False)
        except Exception,e:
            logger.sso.error(e, exc_info=True)
        else:
            logger.sso.info("check login request, cookie_str: %s, success:%s" %(cookie_str, success))
            return success
    else:
        logger.sso.info("Not Logged in")
    return False

def ParseMySQL(mysql, callback="dict"):
    """解析MYSQL配置段"""
    if not mysql:return None
    protocol, dburl = mysql.split("://")
    if "?" in mysql:
        dbinfo, dbargs  = dburl.split("?")
    else:
        dbinfo, dbargs  = dburl, "charset=utf8&timezone=+8:00"
    host,port,user,password,database = dbinfo.split(":")
    charset, timezone = dbargs.split("&")[0].split("charset=")[-1] or "utf8", dbargs.split("&")[-1].split("timezone=")[-1] or "+8:00"
    if callback in ("list", "tuple"):
        return protocol,host,port,user,password,database,charset, timezone
    else:
        return {"Protocol": protocol, "Host": host, "Port": port, "Database": database, "User": user, "Password": password, "Charset": charset, "Timezone": timezone}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.signin:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.signin and g.username in g.api.user_get_admins().get("data", []):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return decorated_function

def UploadImage2Upyun(FilePath, FileData, kwargs=PLUGINS['UpYunStorage']):
    """ Upload image to Upyun Cloud with Api """

    up  = upyun.UpYun(kwargs.get("bucket"), username=kwargs.get("username"), password=kwargs.get("password"), timeout=10, endpoint=upyun.ED_AUTO)
    res = up.put(FilePath, FileData)
    return res

def UploadRealFile2Upyun(file, imgurl, kwargs=PLUGINS['UpYunStorage']):
    """ Upload image to Upyun Cloud with Api """

    up = upyun.UpYun(kwargs.get("bucket"), username=kwargs.get("username"), password=kwargs.get("password"), timeout=10, endpoint=upyun.ED_AUTO)
    formkw = { 'allow-file-type': kwargs.get('allow-file-type', 'jpg,jpeg,png,gif') }
    with open(file, "rb") as f:
        res = up.put(imgurl, f, checksum=True, need_resume=True, form=True, **formkw)
    return res

def BaiduActivePush(pushUrl, original=True, callUrl=PLUGINS['BaiduActivePush']['callUrl']):
    """百度主动推送(实时)接口提交链接"""
    callUrl = callUrl + "&type=original" if original else callUrl
    res = requests.post(url=callUrl, data=pushUrl, timeout=3, headers={"User-Agent": "BaiduActivePush/www.saintic.com"}).json()
    logger.api.info("BaiduActivePush PushUrl is %s, Result is %s" % (pushUrl, res))
    return res

def ChoiceColor():
    """ 模板中随机选择bootstrap内置颜色 """
    color = ["default", "primary", "success", "info", "warning", "danger"]
    return random.choice(color)

def TagRandomColor():
    """ 模板中随机选择颜色 """
    color = ["tagc1", "tagc2", "tagc3", "tagc4", "tagc5"]
    return random.choice(color)

def async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def getIpArea(ip):
    """查询IP地址信息，返回格式：国家 省级 市级 运营商"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
    url = "http://ip.taobao.com/service/getIpInfo.php?ip={0}".format(ip)
    try:
        data = DO(requests.get(url, timeout=10, headers=headers).json())
    except requests.exceptions.Timeout:
        try:
            data = DO(requests.get(url, headers=headers).json())
        except Exception:
            return "Unknown"
        else:
            data = DO(data.data)
    else:
        data = DO(data.data)
    logger.access.debug(data)
    if u'内网IP' in data.city:
        city = data.city
    else:
        if data.city:
            city = data.city if u"市" in data.city else data.city + u"市"
        else:
            city = data.city
    return u"{0} {1} {2} {3}".format(data.country, data.region.replace(u'市',''), city, data.isp)
