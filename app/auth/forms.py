from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_babel import _, lazy_gettext as _l


#  форма входа
class LoginForm(FlaskForm):
    username = StringField(_l('Логин'), validators=[DataRequired()])
    password = PasswordField(_l('Пароль'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Запомнить меня'))
    submit = SubmitField(_l('Войти'))


# форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField(_l('Логин'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Пароль'), validators=[DataRequired()])
    password2 = PasswordField(_l('Повторите пароль'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Зарегистрироваться'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Пользователь с таким логином уже существует'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Пользователь с таким email уже существует'))


# форма сброса пароля
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Запросить сброс пароля'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(_('Пользователя с таким email не существует'))


# форма изменения пароля
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Пароль'), validators=[DataRequired()])
    password2 = PasswordField(_l('Повторите пароль'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Сохранить новый пароль'))



