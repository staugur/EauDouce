# -*- coding: utf8 -*-

import os

GLOBAL={

    "Host": os.getenv("eaudouce_host", "0.0.0.0"),
    #Application run network address, you can set it `0.0.0.0`, `127.0.0.1`, ``.

    "Port": os.getenv("eaudouce_port", 10141),
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


REDIS={

    "SystemIdentification": os.getenv("BlueSky_REDIS_SID", 0),
    #Sid that uniquely identifies cluster nodes

    "ClusterUniqueIdentificationKey": os.getenv("BlueSky_REDIS_CUIK", "bluesky_aliyun"),
    #Uniquely identifies clusters of Key

    "Connection": os.getenv("BlueSky_REDIS_Connection", "redis://ip:port:password")
    #Support redis single or cluster.
    #The single format is redis://ip:port:password;
    #The cluster format is redis_cluster://ip:port,ip2:port,......,ipn:port;
}
