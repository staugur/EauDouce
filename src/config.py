# -*- coding: utf-8 -*-
"""
    EauDouce.config
    ~~~~~~~~~~~~~~

    The program configuration file, the preferred configuration item, reads the system environment variable first.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from os import getenv

GLOBAL = {

    "ProcessName": "EauDouce",
    # 自定义进程名.

    "Host": getenv("eaudouce_host", "0.0.0.0"),
    # 监听地址

    "Port": getenv("eaudouce_port", 10140),
    # 监听端口.

    "LogLevel": getenv("eaudouce_loglevel", "INFO"),
    # 应用日志记录级别, 依次为 DEBUG, INFO, WARNING, ERROR, CRITICAL.
}


MYSQL = getenv("eaudouce_mysql_url")
# MYSQL数据库连接信息
# mysql://host:port:user:password:database?charset=&timezone=


REDIS = getenv("eaudouce_redis_url")
# Redis数据库连接信息，格式：
# redis://[:password]@host:port/db
# host,port必填项,如有密码,记得密码前加冒号,默认localhost:6379/0


RQREDIS = getenv("eaudouce_rqredis_url", REDIS)
# RQ任务队列的Redis数据库连接信息，格式：
# redis://[:password]@host:port/db
# host,port必填项,如有密码,记得密码前加冒号,默认localhost:6379/0


# 认证配置段，需要部署github.com/staugur/passport程序
SSO = {

    "app_name": getenv("eaudouce_sso_app_name", GLOBAL["ProcessName"]),
    # Passport应用管理中注册的应用名

    "app_id": getenv("eaudouce_sso_app_id", "app_id"),
    # Passport应用管理中注册返回的`app_id`

    "app_secret": getenv("eaudouce_sso_app_secret", "app_secret"),
    # Passport应用管理中注册返回的`app_secret`

    "sso_server": getenv("eaudouce_sso_server", "YourPassportFQDN"),
    # Passport部署允许的完全合格域名根地址，例如作者的`https://passport.saintic.com`
}


# 邮箱配置段
EMAIL = {

    "useraddr": getenv("eaudouce_email_useraddr"),
    # 邮箱用户：发件人

    "userpass": getenv("eaudouce_email_userpass"),
    # 用户邮箱密码

    "smtpServer": getenv("eaudouce_email_smtpserver"),
    # 邮箱服务器地址

    "smtpPort": getenv("eaudouce_email_smtpport", 25),
    # 邮箱服务器端口

    "smtpSSL": getenv("eaudouce_email_smtpssl", False)
    # 是否使用SSL加密
}


# picbed图床
PICBED = {
    "enable": getenv("passport_picbed_enable", True),
    "api": getenv("passport_picbed_api"),
    "LinkToken": getenv("passport_picbed_linktoken")
}


# 系统配置
SYSTEM = {

    "HMAC_SHA256_KEY": getenv("eaudouce_hmac_sha256_key", "273d32c8d797fa715190c7408ad73811"),
    # hmac sha256 key

    "AES_CBC_KEY": getenv("eaudouce_aes_cbc_key", "YRRGBRYQqrV1gv5A"),
    # utils.aes_cbc.CBC类中所用加密key

    "JWT_SECRET_KEY": getenv("eaudouce_jwt_secret_key", "WBlE7_#qDf2vRb@vM!Zw#lqrg@rdd3A6"),
    # utils.jwt.JWTUtil类中所用加密key

    "Sign": {
        "version": getenv("eaudouce_sign_version", "v1"),
        "accesskey_id": getenv("eaudouce_sign_accesskeyid", "accesskey_id"),
        "accesskey_secret": getenv("eaudouce_sign_accesskeysecret", "accesskey_secret"),
    }
    # utils.Signature.Signature类中所有签名配置
}


# 内置插件
PLUGINS = {

    "CodeHighlighting": getenv("eaudouce_CodeHighlighting", True),
    # 代码高亮插件

    "ChangyanComment": {
        "enable": getenv("eaudouce_ChangyanComment_enable", False),
        "appid": getenv("eaudouce_ChangyanComment_appid", "app_id"),
        "appkey": getenv("eaudouce_ChangyanComment_appkey", "app_key")
    },
    # 畅言评论系统

    "gitalk": {
        "enable": getenv("eaudouce_gitalk_enable", False),
        "user": getenv("eaudouce_gitalk_user", "staugur"),
        "repo": getenv("eaudouce_gitalk_repo", "EauDouce"),
        "clientId": getenv("eaudouce_gitalk_clientId", "clientId"),
        "clientSecret": getenv("eaudouce_gitalk_clientSecret", "clientSecret")
    },
    # gitalk评论系统

    "Valine": {
        "enable": getenv("eaudouce_valine_enable", False),
        "PLUGINKIT_VALINE_APPID": getenv("eaudouce_valine_appid", "appId"),
        "PLUGINKIT_VALINE_APPKEY": getenv("eaudouce_valine_appkey", "appKey"),
    },
    # valine评论系统，https://valine.js.org

    "ISSO": {
        "enable": getenv("eaudouce_isso_enable", False),
        "api": getenv("eaudouce_isso_api")
    },
    # isso评论系统，https://posativ.org/isso/

    "BaiduStatistics": getenv("eaudouce_BaiduStatistics", False),
    # 百度统计插件

    "BaiduAutoPush": getenv("eaudouce_BaiduAutoPush", False),
    # 百度自动推送插件

    "BaiduActivePush": {
        "enable":  getenv("eaudouce_BaiduActivePush_enable", False),
        "callUrl": getenv("eaudouce_BaiduActivePush_callUrl", "YourCallUrl")
    },
    # 百度主动推送(实时)插件

    "BaiduIncludedCheck": getenv("eaudouce_BaiduIncludedCheck", False),
    # 百度收录检测插件

    "BingIncludedCheck": getenv("eaudouce_BingIncludedCheck", False),
    # 必应收录检测插件

    "UpYunStorage": {
        "enable": getenv("eaudouce_UpYunStorage_enable", False),
        "bucket": getenv("eaudouce_UpYunStorage_bucket", ""),
        "username": getenv("eaudouce_UpYunStorage_username", ""),
        "password": getenv("eaudouce_UpYunStorage_password", ""),
        "dn": getenv("eaudouce_UpYunStorage_dn", ""),
    },
    # 又拍云存储插件

    "LikeReward": getenv("eaudouce_LikeReward", False),
    # 点赞打赏插件

    "AccessCount": getenv("eaudouce_AccessCount", False),
    # 访问统计插件

    "shareJs": getenv("eaudouce_shareJs", False),
    # 社会化分享插件

}
