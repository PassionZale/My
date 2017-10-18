import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'fd9aa8393ca0ee4617214cece3468e8c8d66b1bd4750e08c'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 设置上传目录
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'uploads/')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@ip:port/dbname'
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'data-pro.sqlite')


APP_CONFIG = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'default': DevelopmentConfig
}