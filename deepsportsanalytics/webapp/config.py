import os
import logging

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    UPLOAD_FOLDER = '/tmp'
    LOGGING_FORMAT = '[%(asctime)s] [%(process)d:%(thread)d] [%(levelname)s] [%(module)s] [%(funcName)s] %(message)s'
    LOGGING_LOCATION = '/tmp/deepsportsanalytics.log'
    LOGGING_LEVEL = logging.INFO

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG

class TestConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    MONGO_URI = os.environ.get('MONGOLAB_URI', None)
    REDIS_URL = os.environ.get('REDIS_URL', None)
    AZURE_STORAGE_NAME = os.environ.get('AZURE_STORAGE_NAME', None)
    AZURE_STORAGE_KEY = os.environ.get('AZURE_STORAGE_KEY', None)

__DEF_CONFIG = "deepsportsanalytics.webapp.config.DevelopmentConfig"
__config = {
    "production": "deepsportsanalytics.webapp.config.ProductionConfig",
    "development": "deepsportsanalytics.webapp.config.DevelopmentConfig",
    "testing": "deepsportsanalytics.webapp.config.TestingConfig",
    "default": __DEF_CONFIG
}

def configure_app(app, env):
    app.config.from_object(__config.get(env, __DEF_CONFIG))
    app.config.from_pyfile('config.ini', silent=True)

    # setup logginig
    root_logger = logging.getLogger()
    root_logger.setLevel(app.config['LOGGING_LEVEL'])
    fh = logging.FileHandler(app.config['LOGGING_LOCATION'])
    fh.setLevel(app.config['LOGGING_LEVEL'])
    ch = logging.StreamHandler()
    ch.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    root_logger.addHandler(ch)
    root_logger.addHandler(fh)
    app.logger.addHandler(ch)
    app.logger.addHandler(fh)
