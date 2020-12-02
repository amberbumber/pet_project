# -*- coding: utf-8 -*-
from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler
import os
from datetime import date
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from app.get_token import get_token, test_env
from elasticsearch import Elasticsearch
from threading import Thread
import time


# инициализация объектов


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'  # Значение «login» выше является именем функции (или конечной точки) для входа в систему.\
                            # Другими словами, имя, которое вы будете использовать в вызове url_for(), чтобы получить
                            # URL
login.login_message = _l("Необходимо авторизоваться")
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])  \
        if app.config['ELASTICSEARCH_URL'] else None

    # регистрация схемы данных в приложении
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # логирование ошибок
    if not app.debug and not app.testing:
        # настройка почтового сервера и отправки ошибок
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    #     ADMINS = ['kudryashova@gmail.com']
    #     mail_handler = SMTPHandler('127.0.0.1',
    #                                'server-error@example.com',
    #                                ADMINS, 'YourApplication Failed')
        if not os.path.exists('logs'):
            os.mkdir('logs')
            # if not os.path.exists('logs'+str(date.today())):
            #     os.mkdir('log'+str(date.today()))
            # file_handler = logging.FileHandler('log'+str(date.today())+os.path.sep+'microblog'+str(date.today())+'.log', mode='a',
            #                            encoding='UTF-8')
        file_handler = logging.FileHandler('logs'+ os.path.sep + 'microblog' + str(date.today()) + '.log', mode='a',encoding='UTF-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Microblog startup")



    return app


# выбор предпочтительного языка
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # return 'en'


# получение токена
# def run_thread_get_token():

# th = Thread(target=get_token, args=current_app)
# th.start()
# # print(os.environ.get['IAM_TOKEN'])
# time.sleep(3)
# print(os.environ.get['IAM_TOKEN'])



# print(os.environ.get('TEST_ENV'))
# # os.environ['TEST_ENV']='hello again'
# # print(os.environ.get('TEST_ENV'))




from app import models