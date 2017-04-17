# -*- coding: utf8 -*-

import os

GLOBAL={

    "Host": os.getenv("eaudouce_host", "0.0.0.0"),
    #Application run network address, you can set it `0.0.0.0`, `127.0.0.1`, ``.

    "Port": os.getenv("eaudouce_port", 10140),
    #Application run port, default port.

    "LogLevel": os.getenv("eaudouce_loglevel", "DEBUG"),
    #Application to write the log level, currently has DEBUG, INFO, WARNING, ERROR, CRITICAL.
}


PRODUCT={

    "ProcessName": "EauDouce",
    #Custom process, you can see it with "ps aux|grep ProcessName".

    "ProductType": os.getenv("eaudouce_producttype", "tornado"),
    #Production environment starting method, optional `gevent`, `tornado`.
}


SSO={

    "SSO.URL": os.getenv("eaudouce_ssourl", "https://passport.saintic.com"),
    #The passport(SSO Authentication System) Web Site URL.

    "SSO.PROJECT": PRODUCT["ProcessName"],
    #SSO request application.
}


MYSQL=os.getenv("eaudouce_MYSQL", "mysql://host:port:user:password:database?charset=&timezone=")


PLUGINS={

    "CodeHighlighting": os.getenv("eaudouce_CodeHighlighting", True),
    #代码高亮插件

    "ChangyanComment": {
        "enable": os.getenv("eaudouce_ChangyanComment_enable", True),
        "appid": os.getenv("eaudouce_ChangyanComment_appid", "cysX1azO3"),
        "appkey": os.getenv("eaudouce_ChangyanComment_appkey", "23503a7fdbfe37d50048a5c91d93627d")
    },
    #畅言评论插件

    "BaiduShare": os.getenv("eaudouce_BaiduShare", True),
    #百度分享插件

    "BaiduAutoPush": os.getenv("eaudouce_BaiduAutoPush", True),
    #百度自动推送插件

    "Weather": os.getenv("eaudouce_Weather", True),
    #天气显示插件

    "BaiduStatistics": os.getenv("eaudouce_BaiduStatistics", True),
    #百度统计插件

    "BaiduActivePush": {
        "enable":  os.getenv("eaudouce_BaiduActivePush_enable", False),
        "callUrl": os.getenv("eaudouce_BaiduActivePush_callUrl", "http://data.zz.baidu.com/urls?site=www.saintic.com&token=QbriJ4Iv7TGi8yOF")
    },
    #百度主动实时推送插件

    "BackupBlog": os.getenv("eaudouce_BackupBlog", False),
    #备份文章插件

    "UpYunStorage": {
        "enable": os.getenv("eaudouce_UpYunStorage_enable", False),
        "bucket": os.getenv("eaudouce_UpYunStorage_bucket", ""),
        "username": os.getenv("eaudouce_UpYunStorage_username", ""),
        "password": os.getenv("eaudouce_UpYunStorage_password", ""),
        "secret": os.getenv("eaudouce_UpYunStorage_secret", ""),
        "timeout": os.getenv("eaudouce_UpYunStorage_timeout", 10),
        "dn": os.getenv("eaudouce_UpYunStorage_dn", "https://img.saintic.com"),
        "allow-file-type": "jpg,jpeg,png,gif"
    },
    #又拍云存储插件
}
