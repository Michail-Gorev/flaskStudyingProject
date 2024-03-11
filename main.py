from flask import Flask

import app.constants

first_app = Flask(__name__, static_url_path='/static')

from app import routes

first_app.config['SECRET_KEY'] = app.constants.SECRET_KEY
