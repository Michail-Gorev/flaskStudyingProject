import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "qwerty12345"
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or '587'
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'moisha504@gmail.com'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'moisha504@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'lpcg uqfd aujc iate'
    DATABASE = '/tmp/flask_app.db'
    @staticmethod
    def init_app(app):
            pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestersConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "testers": TestersConfig,
    "production": ProductionConfig
}
