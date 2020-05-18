### 更新于2019-03-13言：

目前更新计划较少，而代码中个性化东西太多（针对个人所有域），所以若拿来就用不适合，待普遍化更新。

# EauDouce
A flask+mysql+bootstrap blog based on personal interests and hobbies.


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
    server_name yourdomainname.com;
    location ~ ^\/static\/.*$ {
        root /xxx/eaudouce/src/;
        access_log off;
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
