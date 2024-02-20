import random

from app import constants
from main import first_app
from flask import render_template, request
from flask import make_response

import app.constants


@first_app.route('/')
def index():
    if request.headers.get('User-Agent') == constants.mozilla_full_spec:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('test_pseudo_random_number', str(random.randint(constants.min_number,
                                                                        constants.max_number)))
    else:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('test_pseudo_random_number', 'Use mozilla to get a number:)')
    return resp


@first_app.route('/set_user/<name>/')
def set_user(name):
    if app.constants.restricted_name in name:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('username', 'error')
    else:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('username', name)
    return resp


@first_app.route('/catalog/')
def show_catalog():
    return render_template("catalog_page.html")


@first_app.route("/profile/", methods=['GET', 'POST'])
def show_profile():
    return render_template('user_page.html')
