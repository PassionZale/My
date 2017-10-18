import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_debugtoolbar import DebugToolbarExtension
from config import APP_CONFIG
# sqlalchemy instance
db = SQLAlchemy()
# uploads instance
photos = UploadSet('photos', IMAGES)
# login_manager instance
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
# debugtoolbar instance
toolbar = DebugToolbarExtension()


def create_app(config_name):
    # app instance
    app = Flask(__name__)
    # config init
    app.config.from_object(APP_CONFIG[config_name])
    APP_CONFIG[config_name].init_app(app)
    # db init
    db.init_app(app)
    # uploads init
    configure_uploads(app, photos)
    # 设置上传文件maximum file size, default is 16MB
    patch_request_class(app)
    # login_manager init
    login_manager.init_app(app)
    # toolbar init
    #toolbar.init_app(app)
    # blueprint init
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .console import console as console_blueprint
    app.register_blueprint(console_blueprint, url_prefix='/console')

    return app