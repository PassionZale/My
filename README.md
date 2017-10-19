# My
单用户简单博客

基于 Flask &amp; Mysql

# 安装及配置
1. 创建数据库(假设数据库名:my)
2. git clone https://github.com/PassionZale/My.git
3. cd My/
4. virtualenv -p /usr/bin/python3 env
5. source ./env/bin/activate
6. pip install -r requirement.txt
7. git update-index --assume-unchanged config.py
8. 打开config.py修改Mysql数据库连接配置 

# 数据库迁移
1. ./manage.py db upgrade
2. 此时数据库中表已创建完毕