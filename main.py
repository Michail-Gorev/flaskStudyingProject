import os
from flask import Flask
from flask_bootstrap import Bootstrap4

import app.constants

DATABASE = '/tmp/flask_app.db'
DEBUG = True

first_app = Flask(__name__)

first_app.config['SECRET_KEY'] = app.constants.SECRET_KEY
first_app.config.from_object(__name__)

first_app.config.update(dict(DATABASE=os.path.join(first_app.root_path, 'flask_app.db')))
bootstrap = Bootstrap4(first_app)

from app import routes
