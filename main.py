from flask import Flask
from flask_bootstrap import Bootstrap4

import app.constants

first_app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap4(first_app)
from app import routes

first_app.config['SECRET_KEY'] = app.constants.SECRET_KEY
