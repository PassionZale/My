from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from app import db, login_manager


# 用户回调函数
@login_manager.user_loader
def user_loader(id):
    return FlaskyConfigs.query.get(int(id))


"""
站点配置模型
包含管理员账户等数据:
    邮箱
    用户名
    密码
    头像
    创建时间
    更新时间
    最后登录时间
"""


class FlaskyConfigs(db.Model, UserMixin):
    __tablename__ = 'flasky_configs'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('密码不是一个可读属性.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Configs(username="%s", email="%s")>' % (self.username,
                                                         self.email)


"""
文章模型
包含文章数据:
    ID
    标题
    内容
    浏览次数
    删除状态
    创建时间
    更新时间
    发布时间
"""


class FlaskyArticles(db.Model):
    __tablename__ = 'flasky_articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    # 浏览次数(PV)
    views = db.Column(db.Integer)
    # 已移至垃圾篓
    drafted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 发布日期
    published_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Articles(titile="%s", views="%s")>' % (self.title, self.views)

    def time_format(self, time):
        if time is not None:
            return time.strftime('%Y-%m-%d %H:%M:%S')
        return None

    def to_json(self):
        json_article = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'views': self.views,
            'drafted': self.drafted,
            'created_at': self.time_format(self.created_at),
            'updated_at': self.time_format(self.updated_at),
            'published_at': self.time_format(self.published_at),
            'link': url_for('console.article_show', id= self.id)
        }
        return json_article