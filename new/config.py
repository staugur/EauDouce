# -*- coding: utf-8 -*-
"""
    EauDouce.config
    ~~~~~~~~~~~~~~

    The program configuration file, the preferred configuration item, reads the system environment variable first.

    :copyright: (c) 2018 by staugur.
    :license: MIT, see LICENSE for more details.
"""

from os import getenv

GLOBAL = {

    "ProcessName": "EauDouce",
    #自定义进程名.

    "Host": getenv("eaudouce_host", "127.0.0.1"),
    #监听地址

    "Port": getenv("eaudouce_port", 10141),
    #监听端口

    "LogLevel": getenv("eaudouce_loglevel", "DEBUG"),
    #应用日志记录级别, 依次为 DEBUG, INFO, WARNING, ERROR, CRITICAL.
}


SSO = {

    "app_name": getenv("eaudouce_sso_app_name", GLOBAL["ProcessName"]),
    # SSO中注册的应用名

    "app_id": getenv("eaudouce_sso_app_id", "app_id"),
    # SSO中注册返回的`app_id`

    "app_secret": getenv("eaudouce_sso_app_secret", "app_secret"),
    # SSO中注册返回的`app_secret`

    "sso_server": getenv("eaudouce_sso_server", "https://passport.saintic.com"),
    # SSO完全合格域名根地址
}


MYSQL = getenv("eaudouce_mysql_url")
#MYSQL数据库连接信息
#mysql://host:port:user:password:database?charset=&timezone=


REDIS = getenv("eaudouce_redis_url")
#Redis数据库连接信息，格式：
#redis://[:password]@host:port/db
#host,port必填项,如有密码,记得密码前加冒号,比如redis://localhost:6379/0


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


#插件配置段
PLUGINS = {}