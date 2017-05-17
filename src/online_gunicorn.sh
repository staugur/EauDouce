#!/bin/bash
#
#使用gunicorn启动, 要求系统安装了gunicorn, gevent
#

dir=$(cd $(dirname $0); pwd)
cd $dir

host="0.0.0.0"
port=$(python -c "from config import GLOBAL;print GLOBAL['Port']")
proc=$(python -c "from config import GLOBAL;print GLOBAL['ProcessName']")
procname="main:app"
cpu_count=$(cat /proc/cpuinfo | grep "processor" | wc -l)
logfile=${dir}/logs/gunicorn.log
pidfile=${dir}/logs/${proc}.pid

case $1 in
start)
    if [ -f $pidfile ]; then
        if [[ $(ps aux | grep $(cat $pidfile) | grep -v grep | wc -l) -lt 1 ]]; then
            gunicorn -w $cpu_count -b ${host}:${port} $procname -k gevent --reload &>> $logfile &
            pid=$!
        fi
    else
        gunicorn -w $cpu_count -b ${host}:${port} $procname -k gevent --reload &>> $logfile &
        pid=$!
    fi
    echo $pid > $pidfile
    echo "$procname start over with pid ${pid}"
    ;;

stop)
    if [ -e $pidfile ];then
        kill -9 $(cat $pidfile) || exit 1
        #for pid in $(ps aux | grep $proc | grep -v grep | awk '{print $2}'); do kill -9 $pid ;done
        rm -f $pidfile
        echo "$procname stop over."
    fi
    ;;

status)
    #pid=$(ps aux | grep $procname | grep -vE "grep|worker|Team.Api\." | awk '{print $2}')
    if [ ! -f $pidfile ]; then
        echo -e "\033[39;31m${procname} has stopped.\033[0m"
        exit
    fi
    pid=$(cat $pidfile)
    procnum=$(ps aux | grep -v grep | grep $pid | grep $procname | wc -l)
    if [[ "$procnum" != "1" ]]; then
        echo -e "\033[39;31m异常，pid文件与系统pid数量不相等。\033[0m"
        echo -e "\033[39;34m  pid数量：${procnum}\033[0m"
        echo -e "\033[39;34m  pid文件：${pid}($pidfile)\033[0m"
    else
        echo -e "\033[39;33m${proc}\033[0m":
        echo "  pid: $pid"
        echo -e "  state:" "\033[39;32mrunning\033[0m"
        echo -e "  process start time:" "\033[39;32m$(ps -eO lstart | grep $pid | grep $procname | grep -vE "worker|grep|Team.Api\." | awk '{print $6"-"$3"-"$4,$5}')\033[0m"
        echo -e "  process running time:" "\033[39;32m$(ps -eO etime| grep $pid | grep $procname | grep -vE "worker|grep|Team.Api\." | awk '{print $2}')\033[0m"
    fi
    ;;

restart)
    sh $0 stop
    sh $0 start
    ;;

*)
    echo "Usage: $0 start|stop|restart|status"
    ;;
esac

