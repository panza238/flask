# este file va a tener todas las configuraciones que antes guardaba como dict en app.config[config_name]
# Todas estas configuraciones las voy a crear como clases.
# Cada aspecto que quiera configurar, va a tener su propia clase.
import os
basedir = os.path.abspath(os.path.dirname(__file__))  # Esto me devuelve el path absoluto del directorio actual.


class Config(object):
    """Esta va a ser la configuración básica.
    El resto de las clases de configuración va a heredar de esta."""
    # Secret Key config (La secret key la usa WTForms para encriptar)
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'hard to guess string'
    # Configuraciones de mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # Config general de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod  # staticmethod me permite usar la función SIN necesidad de instanciar la clase!
    def init_app(app):
        """Este método va a ser necesario. Flask la va a usar."""
        pass


class DevelopmentConfig(Config):
    """Configuraciones para el entorno de desarrollo"""
    DEBUG = True
    # Developmnet DB URI.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                'data-dev.sqlite')


class TestingConfig(Config):
    """Clase para la configuración del entorno de prueba (unittests)"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'


class ProductionConfig(Config):
    """Clase para las configuraciones del entorno de desarrollo"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}

# Bien. Así quedan definidas todas las configuraciones que voy a necesitar!
# A medida que vaya necesitando más configuraciones, voy modificando estas clases que acabo de crear.
