# EauDouce
A flask+mysql+bootstrap blog based on personal interests and hobbies.


#### 更新于2019-03-13言：
目前更新计划较少，而代码中个性化东西太多（针对个人所有域），所以若拿来就用不适合，待普遍化更新。


## Environment
> 1. Python Version: 2.7
> 2. 框架: Flask
> 3. 依赖包: requirements.txt
> 4. 依赖服务: MySQL(必需) Passport(认证)


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
    3.2 sh online_gunicorn.sh start  #生产环境后台启动,采用gunicorn+gevent,不需要额外安装,推荐使用!
    3.3 python super_debug.py        #性能调试模式
```

4. nginx
```
server {
    listen 80;
    listen 443 ssl http2;
    server_name yourdomainname.com www.yourdomainname.com;
    access_log /var/log/nginx/yourdomainname.access.log main;
    if ($host != "www.yourdomainname.com") {
      rewrite ^/(.*)$ https://www.yourdomainname.com/$1 permanent;
    }
    ssl     on;
    ssl_certificate /etc/letsencrypt/live/yourdomainname.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomainname.com/privkey.pem;
    #OCSP Stapling开启,OCSP是用于在线查询证书吊销情况的服务，使用OCSP Stapling能将证书有效状态的信息缓存到服务器，提高TLS握手速度
    ssl_stapling on;
    #OCSP Stapling验证开启
    ssl_stapling_verify on;
    #OCSP Stapling的证书位置
    ssl_trusted_certificate /etc/letsencrypt/live/yourdomainname.com/chain.pem;
    #用于查询OCSP服务器的DNS
    resolver 8.8.8.8 114.114.114.114 valid=300s;
    #查询域名超时时间
    resolver_timeout 5s;
    #SSL优化配置
    #Session Cache，将Session缓存到服务器，这可能会占用更多的服务器资源
    ssl_session_cache builtin:1000 shared:SSL:10m;
    #开启浏览器的Session Ticket缓存
    ssl_session_tickets on;
    #SSL session过期时间
    ssl_session_timeout  10m;
    #只启用 TLS 系列协议
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    #加密套件,这里用了CloudFlare's Internet facing SSL cipher configuration
    #完整参考 ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-RC4-SHA:ECDHE-RSA-RC4-SHA:ECDH-ECDSA-RC4-SHA:ECDH-RSA-RC4-SHA:ECDHE-RSA-AES256-SHA:RC4-SHA:HIGH:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!CBC:!EDH:!kEDH:!PSK:!SRP:!kECDH;
    ssl_ciphers EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!aNULL:!MD5:!RC4:!DHE:!kEDH:!NULL:!ADH:!DH;
    #由服务器协商最佳的加密算法
    ssl_prefer_server_ciphers on;
    #开启HSTS，并设置有效期为9460800秒（9个月），包括子域名(根据情况可删掉)：includeSubdomains，预加载到浏览器缓存(根据情况可删掉)
    add_header Strict-Transport-Security "max-age=15768001; preload";
    #防止在IE9、Chrome和Safari中的MIME类型混淆攻击
    add_header X-Content-Type-Options nosniff;
    #处理静态资源:
    location ~ ^\/static\/.*$ {
        root /xxx/eaudouce/src/;
    }
    location /favicon.ico {
        root /xxx/eaudouce/src/static/img/;
    }
    location / {
       proxy_pass http://127.0.0.1:10140;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       add_header X-Frame-Options SAMEORIGIN;
    }
}
```
