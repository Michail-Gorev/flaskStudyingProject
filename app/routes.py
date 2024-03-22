import random
import sqlite3

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from app import constants
from app.FDataBase import FDataBase
from app.UserLogin import UserLogin
from app.forms import RegistrationForm
from main import first_app
from flask import render_template, request, redirect, url_for, session, g, flash
from flask import make_response
from werkzeug.security import generate_password_hash, check_password_hash
import app.constants

login_manager = LoginManager(first_app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


dbase = None


@first_app.before_request
def before_all():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    connection = sqlite3.connect(first_app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def create_db():
    '''Создание таблицы пользователей данных с помощью выполнения запроса, лежащего в SQL-файле
    Запрос выполняется при условии, что таблица не существует '''
    db = connect_db()
    with first_app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''Соединение с БД'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@first_app.teardown_appcontext
def close_db(e):
    '''Закрытие БД'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@first_app.errorhandler(500)
def server_error_return(e):
    return render_template('500.html'), 500


@first_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@first_app.errorhandler(403)
def user_not_registered(e):
    return render_template('403.html'), 403

@first_app.errorhandler(401)
def user_not_registered(e):
    return render_template('401.html'), 401


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
    return render_template("catalog_page.html", buildings=dbase.getBuildings())


@first_app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        res = dbase.addUser(request.form['username'], request.form['email'],
                            generate_password_hash(request.form['password']), request.form['gender'])
        if res == True:
            return redirect(url_for('login'))
        elif res == "not_unique_email":
            flash("На этот адрес уже зарегистрирован пользователь")
        elif res == "not_unique_username":
            flash("Этот ник уже занят")
    return render_template("registration.html", form=form)


@first_app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = dbase.getUserByUsername(request.form['username'])
        if user and check_password_hash(user['pass_hash'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('show_profile'))
    return render_template("login.html")


@first_app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@first_app.route("/profile/", methods=['GET', 'POST'])
@login_required
def show_profile():
    user = {
        'username': current_user.get_username(),
        'email': current_user.get_email(),
        'gender': current_user.get_gender(),
    }
    return render_template('user_page.html', user=user)
