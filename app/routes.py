import random

from app import constants
from main import first_app
from flask import render_template, request
from flask import make_response

import app.constants


@first_app.errorhandler(500)
def server_error_return(e):
    return render_template('500.html'), 500


@first_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@first_app.errorhandler(403)
def user_not_registered(e):
    return render_template('403.html'), 403


@first_app.route('/')
def index():
    if request.headers.get('User-Agent') == constants.MOZILLA_FULL_SPEC:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('test_pseudo_random_number', str(random.randint(constants.MIN_NUMBER,
                                                                        constants.MAX_NUMBER)))
    else:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('test_pseudo_random_number', 'Use mozilla to get a number:)')
    return resp


@first_app.route('/set_user/<name>/')
def set_user(name):
    if app.constants.RESTRICTED_NAME in name:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('username', 'error')
    else:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('username', name)
    return resp


@first_app.route('/catalog/')
def show_catalog():
    return render_template("catalog_page.html")


@first_app.route('/login/')
def login():
    return render_template("login.html")


@first_app.route("/profile/", methods=['GET', 'POST'])
def show_profile():
    if request.cookies.get('username') is None:
        return user_not_registered(403)
    else:
        return render_template('user_page.html')
