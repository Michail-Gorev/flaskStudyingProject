import random
import sqlite3

from flask import render_template, redirect, url_for, request, flash, make_response, g, current_app
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import main, constants
from .FDataBase import FDataBase
from .UserLogin import UserLogin
from .forms import RegistrationForm
from .. import mail, login_manager
from flask_mail import Message


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


dbase = None


@main.before_request
def before_all():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    connection = sqlite3.connect(current_app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def create_db():
    """Создание таблицы пользователей данных с помощью выполнения запроса, лежащего в SQL-файле
    Запрос выполняется при условии, что таблица не существует """
    db = connect_db()
    with current_app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@main.teardown_app_request
def close_db(e):
    """Закрытие БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@main.route('/')
def index():
    if request.headers.get('User-Agent') == constants.MOZILLA_FULL_SPEC:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('test_pseudo_random_number', str(random.randint(constants.MIN_NUMBER,
                                                                        constants.MAX_NUMBER)))
    else:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('test_pseudo_random_number', 'Use mozilla to get a number:)')
    return resp


@main.route('/set_user/<name>/')
def set_user(name):
    if constants.RESTRICTED_NAME in name:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('username', 'error')
    else:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('username', name)
    return resp


@main.route('/profile/send_prospect/<email>')
def send_prospect(email):
    msg = Message("Test", recipients=[email])
    msg.html = render_template('message.html')
    mail.send(msg)
    return redirect(url_for('main.show_profile'))


@main.route('/catalog/')
def show_catalog():
    return render_template("catalog_page.html", buildings=dbase.getBuildings())


@main.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        res = dbase.addUser(request.form['username'], request.form['email'],
                            generate_password_hash(request.form['password']), request.form['gender'])
        if res:
            return redirect(url_for('main.login'))
        elif res == "not_unique_email":
            flash("На этот адрес уже зарегистрирован пользователь")
        elif res == "not_unique_username":
            flash("Этот ник уже занят")
    return render_template("registration.html", form=form)


@main.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = dbase.getUserByUsername(request.form['username'])
        if user and check_password_hash(user['pass_hash'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('main.show_profile'))
    return render_template("login.html")


@main.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route("/profile/", methods=['GET', 'POST'])
@login_required
def show_profile():
    user = {
        'username': current_user.get_username(),
        'email': current_user.get_email(),
        'gender': current_user.get_gender(),
    }
    return render_template('user_page.html', user=user)
