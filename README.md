# EauDouce
A flask+mysql+bootstrap blog based on personal interests and hobbies.

## LICENSE
MIT

## Environment
> 1. Python Version: 2.7
> 2. 框架: Flask
> 3. 依赖包:

```
Flask==0.10.1
Flask-RESTful
SpliceURL>=1.2
MySQL-python>=1.2.3
torndb>=0.3
requests
beautifulsoup4
upyun
redis
setproctitle
gunicorn
gevent
uwsgi
```
> 4. 依赖服务:

```
1. MySQL(必需)
2. Passport
```

## Usage

```

0. Deploy Passport:
    Please redirect to https://github.com/staugur/passport

1. Requirement:
    1.0 yum install -y gcc gcc-c++ python-devel libffi-devel openssl-devel mysql-devel
    1,1 git clone https://github.com/staugur/EauDouce && cd EauDouce
    1.2 pip install -r requirements.txt

2. modify config.py or add environment variables(os.getenv key in the reference configuration item):

3. run:
    3.0 cd src
    3.1 python main.py               #开发环境启动
    3.2 python -O online_gevent.py   #生产环境前台启动,采用gevent,不需要额外安装,可使用supervisor守护
    3.3 python -O online_tornado.py  #生产环境前台启动,采用tornado,需要安装:pip install tornado,可使用supervisor守护
    3.4 sh online_uwsgi.sh start     #生产环境后台启动,采用uwsgi,不需要额外安装,推荐使用!
    3.5 sh online_gunicorn.sh start  #生产环境后台启动,采用gunicorn+gevent,不需要额外安装,推荐使用!
    3.6 python super_debug.py        #性能调试模式

4. nginx

server {
    listen 80 default;
    server_name www.saintic.com saintic.com;
    charset utf-8;
    access_log           logs/www.access.log main;
    rewrite ^/(.*)$ https://www.saintic.com/$1 permanent;
}
server {
    listen 443 ssl;
    server_name www.saintic.com saintic.com;
    charset utf-8;
    access_log           logs/www.access.log main;
    ssl     on;
    ssl_certificate      /etc/letsencrypt/live/saintic.com/fullchain.pem;
    ssl_certificate_key  /etc/letsencrypt/live/saintic.com/privkey.pem;
    location / {
       proxy_pass http://127.0.0.1:10140;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_headers_hash_max_size 51200;
       proxy_headers_hash_bucket_size 6400;
    }
    location /static {
        root /data/github/eaudouce/src/;
    }
    location ~.*\.(js|css|jpeg|png|jpg)$ {
        root /data/github/eaudouce/src/;
        expires    3d;
    }
}
```
亦可参考：[http://www.saintic.com/blog/201.html](http://www.saintic.com/blog/201.html "http://www.saintic.com/blog/201.html")

## Plugin

## Design
![Design][1]

[1]: ./misc/design.png

