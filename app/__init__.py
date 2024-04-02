import os

from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager
from flask_mail import Mail
from config import config

bootstrap = Bootstrap4()
mail = Mail()
login_manager = LoginManager()

DATABASE = '/tmp/flask_app.db'
DEBUG = True


def create_app(config_name="development"):
    first_app = Flask(__name__)
    first_app.config.from_object(config[config_name])
    config[config_name].init_app(first_app)

    from .main import main as main_blueprint
    first_app.register_blueprint(main_blueprint)

    bootstrap.init_app(first_app)
    mail.init_app(first_app)
    login_manager.init_app(first_app)
    first_app.config.update(dict(DATABASE=os.path.join(first_app.root_path, 'flask_app.db')))

    return first_app
