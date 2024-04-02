from flask import render_template
from . import main


@main.errorhandler(500)
def server_error_return(e):
    return render_template('500.html'), 500


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(403)
def user_not_registered(e):
    return render_template('403.html'), 403


@main.errorhandler(401)
def user_not_registered(e):
    return render_template('401.html'), 401