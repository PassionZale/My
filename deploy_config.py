import os
bind='127.0.0.1:8001' #绑定的端口
workers=4 #worker数量
backlog=2048
debug=True
proc_name='gunicorn.pid'
pidfile='/var/log/gunicorn/debug.log'
loglevel='debug'
