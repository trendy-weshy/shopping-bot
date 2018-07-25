
import os
import logging

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_URI', default='mongodb://localhost:27017/voke-db')
    }

    SECRET_KEY = 'ZAL3mnEt+LiE8U7HfN20Bw=='

    DEBUG = False
    TESTING = False

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "tiYsCOHmBQFEACxBnLU="

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False

    MAIL_SERVER = os.environ.get('SMTP_HOST_ADDRESS')
    MAIL_PORT = os.environ.get('SMTPL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('SMTP_EMAIL_ADDRESS')
    MAIL_PASSWORD = os.environ.get('SMTP_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[VOKE_MAILS]'
    MAIL_SENDER = os.getenv('SMTP_EMAIL_ADDRESS', default='trendy.60.box@gmail.com')

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    PREFERRED_URL_SCHEME = 'https'
    DEBUG = False
    SECURITY_PASSWORD_SALT = 'CoRaGZ6VB9rL3qxHuiA04taSu1yX37QNWhWTty8QQZKfl6gFcYFC9KisIXX/Ms4pRDQrDA2TLgUUvQvVabjd+g' \
                             '/8XIPdXc7bx4FIDFFI7OCKJHR0 '
    SECRET_KEY = 'Efxm0VUSZ9r6Um/N0FMU6P8g/gXS' \
                 '/SpCYbeqDoyRWbeN5R2ppsUwsPd0puFveW1Be9YLvL4EJrte3cZw5VOdTmKUqqskI4tUdMHdykdFzOnfqaJxWTd1GnvP/nmN4k2J '

    @classmethod
    def init_app(cls, app):
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    MAIL_DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}[os.getenv('PYTHON_ENV', default='development')]
