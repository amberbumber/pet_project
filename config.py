import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # переменные для бд
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # настройки почтового сервера
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['asrel-atlas@yandex.ru']

    # количество постов на 1 странице при разбиении
    POSTS_PER_PAGE = 5

    # список поддерживаемых языков
    LANGUAGES = ['ru', 'en']

    # токен для доступа к Yandex.Translate
    IAM_TOKEN = os.environ.get('IAM_TOKEN')

    # конфигурация elasticsearch
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # ведение журнала в stdout
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # URL-адрес подключения к службе Redis
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'


