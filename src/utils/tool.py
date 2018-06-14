# -*- coding: utf-8 -*-
"""
    EauDouce.utils.tool
    ~~~~~~~~~~~~~~

    Common function.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import os, re, requests, hashlib, datetime, random, upyun, time, hmac
from uuid import uuid4
from log import Logger
from base64 import b32encode
from config import PLUGINS, SYSTEM

class DO(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

###===~~~
ip_pat          = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
mail_pat        = re.compile(r"([0-9a-zA-Z\_*\.*\-*]+)@([a-zA-Z0-9\-*\_*\.*]+)\.([a-zA-Z]+$)")
user_pat        = re.compile(r'[a-zA-Z\_][0-9a-zA-Z\_]')
comma_pat       = re.compile(r"\s*,\s*")
logger          = DO(
                    sys = Logger("sys").getLogger,
                    api = Logger("api").getLogger,
                    err = Logger("error").getLogger,
                    access = Logger("access").getLogger,
                    plugin = Logger("plugin").getLogger
                  )
md5             = lambda pwd:hashlib.md5(pwd).hexdigest()
hmac_sha256     = lambda message: hmac.new(key=SYSTEM["HMAC_SHA256_KEY"], msg=message, digestmod=hashlib.sha256).hexdigest()
gen_token       = lambda n=32:b32encode(uuid4().hex)[:n]
gen_requestId   = lambda :str(uuid4())
get_today       = lambda format="%Y-%m-%d %H:%M":datetime.datetime.now().strftime(format)
gen_rnd_filename= lambda :"%s%s" %(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randrange(1000, 10000)))
ListEqualSplit  = lambda l,n=5: [ l[i:i+n] for i in range(0,len(l), n) ]


def ip_check(ip):
    if isinstance(ip, (str, unicode)):
        return ip_pat.match(ip)

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
    res = dict(success=0)
    callUrl = callUrl + "&type=original" if original else callUrl
    try:
        res = requests.post(url=callUrl, data=pushUrl, timeout=3, headers={"User-Agent": "BaiduActivePush/www.saintic.com"}).json()
    except Exception,e:
        logger.api.warning(e, exc_info=True)
    else:
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
    if u'内网IP' in data.city:
        city = data.city
    else:
        if data.city:
            city = data.city if u"市" in data.city else data.city + u"市"
        else:
            city = data.city
    return u"{0} {1} {2} {3}".format(data.country, data.region.replace(u'市',''), city, data.isp)

def get_current_timestamp():
    """ 获取本地当前时间戳(10位): Unix timestamp：是从1970年1月1日（UTC/GMT的午夜）开始所经过的秒数，不考虑闰秒 """
    return int(time.mktime(datetime.datetime.now().timetuple()))

def timestamp_after_timestamp(timestamp=None, seconds=0, minutes=0, hours=0, days=0):
    """ 给定时间戳(10位),计算该时间戳之后多少秒、分钟、小时、天的时间戳(本地时间) """
    # 1. 默认时间戳为当前时间
    timestamp = get_current_timestamp() if timestamp is None else timestamp
    # 2. 先转换为datetime
    d1 = datetime.datetime.fromtimestamp(timestamp)
    # 3. 根据相关时间得到datetime对象并相加给定时间戳的时间
    d2 = d1 + datetime.timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    # 4. 返回某时间后的时间戳
    return int(time.mktime(d2.timetuple()))

def timestamp_to_timestring(timestamp, format='%Y-%m-%d %H:%M:%S'):
    """ 将时间戳(10位)转换为可读性的时间 """
    # timestamp为传入的值为时间戳(10位整数)，如：1332888820
    timestamp = time.localtime(timestamp)
    # 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    return time.strftime(format, timestamp)

def url_check(addr):
    """检测UrlAddr是否为有效格式，例如
    http://ip:port
    https://abc.com
    """
    regex = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if addr and isinstance(addr, (str, unicode)):
        if regex.match(addr):
            return True
    return False

def sql_safestring_check(string):
    """检查拼接sql的字符串是否安全
    诸如：含有问号、逗号、分号、百分号、转义符不予通过
    返回：True代表安全，False表示不安全
    """
    if string:
        if "'" in string or '"' in string or '?' in string or '%' in string or ';' in string or '*' in string or '=' in string or "\\" in string or "_" in string:
            return False
    return True

def make_zipfile(zip_filename, zip_path, exclude=[]):
    """Create a zipped file with the name zip_filename. Compress the files in the zip_path directory. Do not include subdirectories. Exclude files in the exclude file.
    @param zip_filename str: Compressed file name
    @param zip_path str: The compressed directory (the files in this directory will be compressed)
    @param exclude list,tuple: File suffixes will not be compressed in this list when compressed
    """
    if zip_filename and os.path.splitext(zip_filename)[-1] == ".zip" and zip_path and os.path.isdir(zip_path) and isinstance(exclude, (list, tuple)):
        try:
            import zipfile
        except ImportError:
            raise
        with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for filename in os.listdir(zip_path):
                if os.path.isdir(filename):
                    continue
                if not os.path.splitext(filename)[-1] in exclude:
                    zf.write(os.path.join(zip_path, filename), filename)
        return zip_filename if os.path.isabs(zip_filename) else os.path.join(os.getcwd(), zip_filename)
    else:
        raise TypeError
