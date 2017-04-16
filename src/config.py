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

    "CodeHighlighting": os.getenv("Interest_blog_CodeHighlighting", True),
    #代码高亮插件

    "DuoshuoComment": {
        "enable": os.getenv("Interest_blog_DuoshuoComment_enable", False),
        "shortName": os.getenv("Interest_blog_DuoshuoComment_shortName", "saintic")
    },
    #多说评论插件

    "Weather": os.getenv("Interest_blog_Weather", True),
    #天气显示插件

    "BaiduAutoPush": os.getenv("Interest_blog_BaiduAutoPush", True),
    #百度自动推送插件

    "BaiduActivePush": {
        "enable":  os.getenv("Interest_blog_BaiduActivePush_enable", True),
        "callUrl": os.getenv("Interest_blog_BaiduActivePush_callUrl", "http://data.zz.baidu.com/urls?site=www.saintic.com&token=QbriJ4Iv7TGi8yOF")
    },
    #百度主动推送(实时)插件

    "BaiduStatistics": os.getenv("Interest_blog_BaiduStatistics", True),
    #百度统计插件

    "BaiduShare": os.getenv("Interest_blog_BaiduShare", True),
    #百度分享插件

    "BackupBlog": os.getenv("Interest_blog_BackupBlog", False),
    #备份文章插件

    "UpYunStorage": {
        "enable": os.getenv("Interest_blog_UpYunStorage_enable", False),
        "bucket": os.getenv("Interest_blog_UpYunStorage_bucket", ""),
        "username": os.getenv("Interest_blog_UpYunStorage_username", ""),
        "password": os.getenv("Interest_blog_UpYunStorage_password", ""),
        "secret": os.getenv("Interest_blog_UpYunStorage_secret", ""),
        "timeout": os.getenv("Interest_blog_UpYunStorage_timeout", 10),
        "dn": os.getenv("Interest_blog_UpYunStorage_dn", "https://img.saintic.com"),
        "allow-file-type": "jpg,jpeg,png,gif"
    },
    #又拍云存储插件

    "ChristmasBlessings": os.getenv("Interest_blog_ChristmasBlessings", False),
    #圣诞节祝福插件

    "360AutoPush": os.getenv("Interest_blog_360AutoPush", True),
    #360自动推送插件

    "ShowGitHub": os.getenv("Interest_blog_ShowGitHub", False),
    #个人中心页展现GitHub代码库插件，最多展现49个
}
