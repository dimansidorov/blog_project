import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '3a+*q6&rjy0#6^57w#6j&+j0lol_$nh*=4$^d*(@2m%r@lnis%'
    WTF_CSRF_ENABLED = True
    FLASK_ADMIN_SWATCH = 'cerulean'


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    TESTING = True
