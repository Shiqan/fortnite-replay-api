import os

DATABASE_URL = os.environ.get('DATABASE_URL')

class BaseConfig:
    """ Base configuration """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class DevelopmentConfig(BaseConfig):
    """ Development configuration """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class TestConfig(BaseConfig):
    """ Test configuration """
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    """ Production configuration """
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
