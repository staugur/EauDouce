# -*- coding: utf-8 -*-
"""
    EauDouce.config
    ~~~~~~~~~~~~~~

    The program configuration file, the preferred configuration item, reads the system environment variable first.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import os

GLOBAL={

    "ProcessName": "EauDouce",
    #自定义进程名.

    "Port": os.getenv("eaudouce_port", 10140),
    #应用绑定的Port.

    "LogLevel": os.getenv("eaudouce_loglevel", "DEBUG"),
    #应用日志记录级别, 依次为 DEBUG, INFO, WARNING, ERROR, CRITICAL.
}


SSO={

    "SSO.URL": os.getenv("eaudouce_ssourl", "https://passport.saintic.com"),
    #认证中心地址

    "SSO.PROJECT": GLOBAL["ProcessName"],
}


MYSQL=os.getenv("eaudouce_mysql_url")
#MYSQL数据库连接信息
#mysql://host:port:user:password:database?charset=&timezone=


REDIS=os.getenv("eaudouce_redis_url")
#Redis数据库连接信息，格式：
#redis://[:password]@host:port/db
#host,port必填项,如有密码,记得密码前加冒号,默认localhost:6379/0


PLUGINS={

    "CodeHighlighting": os.getenv("eaudouce_CodeHighlighting", True),
    #代码高亮插件

    "ChangyanComment": {
        "enable": os.getenv("eaudouce_ChangyanComment_enable", False),
        "appid": os.getenv("eaudouce_ChangyanComment_appid", "cysX1azO3"),
        "appkey": os.getenv("eaudouce_ChangyanComment_appkey", "23503a7fdbfe37d50048a5c91d93627d")
    },
    #畅言评论插件

    "BaiduShare": os.getenv("eaudouce_BaiduShare", True),
    #百度分享插件

    "BaiduStatistics": os.getenv("eaudouce_BaiduStatistics", False),
    #百度统计插件

    "BaiduAutoPush": os.getenv("eaudouce_BaiduAutoPush", True),
    #百度自动推送插件
    
    "BaiduActivePush": {
        "enable":  os.getenv("eaudouce_BaiduActivePush_enable", False),
        "callUrl": os.getenv("eaudouce_BaiduActivePush_callUrl", "http://data.zz.baidu.com/urls?site=www.saintic.com&token=QbriJ4Iv7TGi8yOF")
    },
    #百度主动推送(实时)插件

    "BaiduIncludedCheck": os.getenv("eaudouce_BaiduIncludedCheck", True),
    #百度收录检测插件

    "Weather": os.getenv("eaudouce_Weather", True),
    #天气显示插件

    "BackupBlog": os.getenv("eaudouce_BackupBlog", False),
    #备份文章插件,如果开启了又拍云存储插件,将会存储到又拍云上,否则存到本地

    "UpYunStorage": {
        "enable": os.getenv("eaudouce_UpYunStorage_enable", False),
        "bucket": os.getenv("eaudouce_UpYunStorage_bucket", ""),
        "username": os.getenv("eaudouce_UpYunStorage_username", ""),
        "password": os.getenv("eaudouce_UpYunStorage_password", ""),
        "dn": os.getenv("eaudouce_UpYunStorage_dn", "https://img.saintic.com"),
    },
    #又拍云存储插件

    "Like": os.getenv("eaudouce_Like", True),
    #点赞插件

    "Reward": os.getenv("eaudouce_Reward", True),
    #打赏插件
}
