# EauDouce
A flask+mysql+bootstrap blog based on personal interests and hobbies.

## LICENSE
MIT

## Environment
> 1. Python Version: 2.7
> 2. Web Framework: Flask
> 3. Required Modules:

```
Flask==0.10.1
tornado
gevent
setproctitle
requests
torndb
MySQL-python
SpliceURL>=1.2
upyun>=2.4.2
#sh
#uwsgi
#如果你打算生产环境使用uwsgi启动，那么去掉这两个注释。
```

## Usage

```

0. Depend:
    0.0 Deploy Api(https://github.com/staugur/Api)
    0.1 Deploy Passport(https://github.com/staugur/passport)

1. Requirement:
    1.0 yum install -y gcc gcc-c++ python-devel libffi-devel openssl-devel
    1.1 pip install -r requirements.txt

2. modify config.py or add environment variables(os.getenv key in the reference configuration item):

3. run:
    3.1 python main.py        #Develop Mode
    3.2 sh Control.sh         #Product Mode
    3.3 python -O Product.py  #Product Mode
    3.4 python super_debug.py #SuperDebug Mode

```
亦可参考：[http://www.saintic.com/blog/201.html](http://www.saintic.com/blog/201.html "http://www.saintic.com/blog/201.html")

## Design
![Design][1]

[1]: ./misc/design.png

