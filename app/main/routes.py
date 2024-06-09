import random
import sqlite3

import jwt
from flask import render_template, redirect, url_for, request, flash, make_response, g, current_app, jsonify
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import main, constants
from .FDataBase import FDataBase
from .UserLogin import UserLogin
from .forms import RegistrationForm
from .. import mail, login_manager
from flask_mail import Message

private_key = open('private.pem').read()
public_key = open('public.pem').read()


@login_manager.user_loader
def load_user(user_id):
    """
    Returns user's info by it's id
    :param user_id: id of user to be returned
    :return: user's info
    """
    return UserLogin().fromDB(user_id, dbase)


dbase = None


@main.before_request
def before_all():
    """
    Prepares DB to be used
    """
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    """
    Open connection with DB
    """
    connection = sqlite3.connect(current_app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def create_db():
    """Create users table, if it doesn't exist"""
    db = connect_db()
    with current_app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Connection with DB"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@main.teardown_app_request
def close_db(e):
    """Closure of DB connection"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@main.before_request
def before_request():
    """Checks whether username is in cookies of current session to load particular user"""
    g.user = None
    if 'username' in request.cookies:
        username = request.cookies['username']
        print(username)
        cursor = get_db().cursor()
        cursor.execute(f"SELECT * FROM user WHERE username = '{username}'")
        user = cursor.fetchone()
        cursor.close()
        g.user = user
        print(g.user['role_id'])


@main.route('/')
def index():
    """
    Sets a pseudo-random number to cookie, if mozilla used,
    and suggests to use mozilla browser in other case.
    """
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
    """
    Sets provided name to cookie
    :param name: name, which is needed to be saved in cookie
    """
    if constants.RESTRICTED_NAME in name:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('username', 'error')
    else:
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('username', name)
    return resp


@main.route('/profile/send_prospect/<email>')
def send_prospect(email):
    """
    Sends the greeting email to provided email address
    :param email: email, to which the message should be sent
    """
    msg = Message("Test", recipients=[email])
    msg.html = render_template('message.html')
    mail.send(msg)
    return redirect(url_for('main.show_profile'))


@main.route('/catalog/')
def show_catalog():
    """
    Renders the houses page
    :return:  the houses page with their names and pictures
    """
    return render_template("catalog_page.html", buildings=dbase.getBuildings())


@main.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Provides registration page with registration form. Checks all fields to be
    correctly filled and then create user with corresponding params
    :return: login page if registration is successful
    """
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        res = dbase.addUser(request.form['username'], request.form['email'],
                            generate_password_hash(request.form['password']), request.form['gender'], 0)
        if res == True:
            token = jwt.encode({'email': email}, private_key, algorithm='RS256')
            data = {
                'token': token
            }
            msg = Message("Test", recipients=[email])
            msg.html = render_template('confirm.html', data=data)
            mail.send(msg)
            return jsonify({'success': True, 'message': 'Регистрация успешна. Проверьте свою почту для подтверждения.'})
        elif res == "not_unique_email":
            flash("На этот адрес уже зарегистрирован пользователь")
        elif res == "not_unique_username":
            flash("Этот ник уже занят")
    return render_template("registration.html", form=form)


@main.route('/register/confirm/<token>')
def confirm_registration(token):
    """
    Confirms registration after user has been tap to confirmation link
    :param token: secure token to confirm email
    """
    try:
        # Проверьте и подтвердите токен JWT
        payload = jwt.decode(token, public_key, algorithms=['RS256'])
        email = payload['email']

        # Найдите и активируйте пользователя по email
        dbase.confirmUserByEmail(email)
        return redirect(url_for('main.login'))
    except jwt.exceptions.InvalidTokenError:
        return jsonify({'error': 'Недействительный токен'}), 401


@main.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Provides login page with login form. Checks all fields to be
    correctly filled and then open user's profile
    :return: profile page if login is successful
    """
    if request.method == 'POST':
        user = dbase.getUserByUsername(request.form['username'])
        if user and check_password_hash(user['pass_hash'], request.form['password']) and user['is_confirmed'] == 1:
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            resp = make_response(redirect(url_for('main.show_profile')))
            resp.set_cookie('username', user['username'])
            return resp
    return render_template("login.html")


@main.route('/logout/')
@login_required
def logout():
    """
    Logs out current user
    :return: login page
    """
    logout_user()
    return redirect(url_for('main.login'))


@main.route("/profile/", methods=['GET', 'POST'])
@login_required
def show_profile():
    """
    Renders profile page with all information about the user
    """
    user = {
        'username': current_user.get_username(),
        'email': current_user.get_email(),
        'gender': current_user.get_gender(),
        'is_confirmed': current_user.get_is_confirmed(),
        'role_id': current_user.get_role_id(),
    }
    if not int(current_user.get_is_confirmed()) == 1:
        return render_template('401.html'), 401
    else:
        return render_template('user_page.html', user=user)


@main.route("/admin/")
def admin_page():
    """
    Render admin page with admin menu section
    :return: admin page
    """
    if g.user is not None and g.user['role_id'] == 1:
        return render_template('401.html'), 401
    else:

        return render_template('admin_page.html')


@main.route("/admin/users/")
def admin_show_users():
    """
    Renders table of users
    """
    if g.user is not None and g.user['role_id'] == 1:
        return render_template('401.html'), 401
    else:
        users = dbase.getUsers()
        return render_template('admin_users.html', users=users)


@main.route("/admin/delete/<username>")
def admin_delete(username):
    """
    Deletes user from DB by their username
    :param username: username of an entity to be deleted
    """
    if g.user is not None and g.user['role_id'] == 1:
        return render_template('401.html'), 401
    else:
        dbase.deleteUser(username)
        return redirect("/admin/users/")


@main.route("/admin/edit/<username>")
def admin_edit_user(username):
    """
    Redirects to user information editor page
    :param username: username of an entity to be edited
    """
    if g.user is not None and g.user['role_id'] == 1:
        return render_template('401.html'), 401
    else:
        user = dbase.getUserByUsername(username)
        return render_template("admin_edit_user.html", user=user)


@main.route("/admin/edit/update", methods=['GET', 'POST'])
def admin_edit_user_update():
    """
    Sends an update request to DB to refresh user data
    """
    if g.user is not None and g.user['role_id'] == 1:
        return render_template('401.html'), 401
    else:
        if request.method == 'POST':
            username = request.form['username']
            field_to_change = request.form['field_to_change']
            new_value = request.form['new_value']
            dbase.editUser(field_to_change, new_value, username)
            user = dbase.getUserByUsername(username)
        return render_template("admin_edit_user.html", user=user)