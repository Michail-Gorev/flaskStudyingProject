from wtforms import Form, StringField, PasswordField, validators, SelectField, widgets


class RegistrationForm(Form):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25)], name='username')
    email = StringField('Email', [validators.Length(min=6, max=35)], name='email')
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ], name='password')
    confirm = PasswordField('Повторите пароль')
    gender = SelectField(label='Укажите пол', default='Не указано',
                         choices=['Не указано', 'Мужской', 'Женский', 'Attack helicopter'], name='gender')
