#!/bin/bash
#
#使用uwsgi启动, 要求系统安装了uwsgi, 可以pip install uwsgi，也可以编译安装、yum安装
#

dir=$(cd $(dirname $0); pwd)
cd $dir

host="0.0.0.0"
port=$(python -c "from config import GLOBAL;print GLOBAL['Port']")
proc=$(python -c "from config import GLOBAL;print GLOBAL['ProcessName']")
procname=$proc
cpu_count=$(cat /proc/cpuinfo | grep "processor" | wc -l)
logfile=${dir}/logs/uwsgi.log
pidfile=${dir}/logs/${proc}.pid
[ -d ${dir}/logs ] || mkdir -p ${dir}/logs

case $1 in
start)
    if [ -f $pidfile ]; then
        echo "Has pid($(cat $pidfile)) in $pidfile, please check, exit." ; exit 1
    else
        uwsgi --http ${host}:${port} --module main --callable app --master --procname-master ${proc}.master --procname ${proc}.worker -p $cpu_count --chdir $dir --threads 2 &>> $logfile &
        pid=$!
        echo $pid > $pidfile
        echo "$procname start over with pid ${pid}"
    fi
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
        echo -e "\033[39;33m${procname}\033[0m":
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

