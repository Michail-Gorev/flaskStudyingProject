import os
from flask import Flask
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap4

import app.constants

DATABASE = '/tmp/flask_app.db'
DEBUG = True

first_app = Flask(__name__)

first_app.config['SECRET_KEY'] = app.constants.SECRET_KEY
first_app.config['MAIL_SERVER'] = app.constants.MAIL_SERVER
first_app.config['MAIL_PORT'] = app.constants.MAIL_PORT
first_app.config['MAIL_USE_TLS'] = app.constants.MAIL_USE_TLS
first_app.config['MAIL_USERNAME'] = app.constants.MAIL_USERNAME
first_app.config['MAIL_DEFAULT_SENDER'] = app.constants.MAIL_DEFAULT_SENDER
first_app.config['MAIL_PASSWORD'] = app.constants.MAIL_PASSWORD

first_app.config.from_object(__name__)

first_app.config.update(dict(DATABASE=os.path.join(first_app.root_path, 'flask_app.db')))
bootstrap = Bootstrap4(first_app)


from app import routes
