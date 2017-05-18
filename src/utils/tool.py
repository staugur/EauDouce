# -*- coding: utf8 -*-

import re, requests, hashlib, datetime, random, upyun
from uuid import uuid4
from log import Logger
from base64 import b32encode
from config import SSO, PLUGINS
from functools import wraps
from flask import g, request, redirect, url_for
from bs4 import BeautifulSoup

ip_pat          = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
mail_pat        = re.compile(r"([0-9a-zA-Z\_*\.*\-*]+)@([a-zA-Z0-9\-*\_*\.*]+)\.([a-zA-Z]+$)")
user_pat        = re.compile(r'[a-zA-Z\_][0-9a-zA-Z\_]')
comma_pat       = re.compile(r"\s*,\s*")
logger          = Logger("sys").getLogger
sso_logger      = Logger("sso").getLogger
access_logger   = Logger("access").getLogger
md5             = lambda pwd:hashlib.md5(pwd).hexdigest()
gen_token       = lambda n=32:b32encode(uuid4().hex)[:n]
gen_requestId   = lambda :str(uuid4())
get_today       = lambda :datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
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
            logger.error(e, exc_info=True)
        else:
            logger.info("check login request, cookie_str: %s, success:%s" %(cookie_str, success))
            return success
    else:
        logger.info("Not Logged in")
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

def ParseRedis(redis):
    """解析REDIS配置段"""
    if not redis:return None
    protocol, dburl = redis.split("://")
    #["redis", "host:port:password@db"], ["redis_cluster", "host:port,host:port"]
    if protocol == "redis":
        if "@" in dburl:
            dbinfo, db = dburl.split("@")
            #["host:port:password", "db"]
        else:
            db = 0
            dbinfo = dburl.split("@")[0]
            #["host:port:password", 0]
        if len(dbinfo.split(":")) == 2:
            password = None
            host, port = dbinfo.split(":")
        else:
            host, port, password = dbinfo.split(":")
        data = {"host": host, "port": port, "password": password, "db": db}

    elif protocol == "redis_cluster":
        dbinfo = re.split(comma_pat, dburl)
        #['host:port', 'host:port']
        data = [ {"host": i.split(":")[0], "port": i.split(":")[-1] } for i in dbinfo ]

    logger.debug("REDIS INFO: {}".format(data))
    return data
        
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

def BaiduActivePush(pushUrl, original=True, callUrl=PLUGINS['BaiduActivePush']['callUrl']):
    """百度主动推送(实时)接口提交链接"""
    callUrl = callUrl + "&type=original" if original else callUrl
    res = requests.post(url=callUrl, data=pushUrl, timeout=3, headers={"User-Agent": "BaiduActivePush/www.saintic.com"}).json()
    logger.info("BaiduActivePush PushUrl is %s, Result is %s" % (pushUrl, res))
    return res

def BaiduIncludedCheck(url):
    """
    get baidu serp links with the url
    """
    # 设置UA模拟用户，还可设置多个UA提高搜索成功率
    headers = {'User-Agent': 'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)'}
    # 构建百度搜索URL；因为是查收录，所以只显示了前10个搜索结果，还可以通过rn参数来调整搜索结果的数量
    b_url = 'http://www.baidu.com/s?wd=%s&rn=1' % url
    # 初始化BeautifulSoup
    soup = BeautifulSoup(requests.get(b_url, headers=headers, timeout=2).content, "html.parser")
    # 获取URL的特征值是通过class="t"
    b_links = [tag.a['href'] for tag in soup.find_all('h3', {'class': 't'})]
    # 分析搜索结果中的真实URL,使用requests库获取了最终URL，而不是快照URL
    real_links = []
    for link in b_links:
        try:
            r = requests.get(link, headers=headers, timeout=2)
        except Exception as e:
            pass
        else:
            print r.status_code,r.url
            real_links.append(r.url)
    #待查URL是否在百度搜索结果的真实URL列表中，如果在就表示收录，反之未收录
    if url in real_links:
        return True
    else:
        return False
