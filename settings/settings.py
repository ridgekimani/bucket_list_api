import os


class Config(object):
    """
    Main configuration object
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '3caaa0a7-7d1c-430f-84e3-1161cdff1b0b'
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = "postgresql://bucket_list:bucket_list@localhost/bucket_list_db"
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Configuration for the deployment"
    """
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Configuration while developing locally
    """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """
    Configuration for testing
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://bucket_list:bucket_list@localhost/test_bucket_list"
    TESTING = True


app_config = {
    'development': 'settings.settings.DevelopmentConfig',
    'testing': 'settings.settings.TestingConfig',
    'production': 'settings.settings.ProductionConfig'
}
