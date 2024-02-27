from flask import Flask


first_app = Flask(__name__, static_url_path='/static')

from app import routes