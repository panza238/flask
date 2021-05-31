from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    """Esta app es mi application factory. Crea la app con la configuración que necesito.
    Como parámetro, se le pasa el nombre de la config que se quiere utilizar
    En este caso, las posibles opciones serían: test, development, production"""
    app = Flask(__name__)  # acá instancio la app.
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)  # estas dos líneas son de import de configuraciones
    # Inicializo lo que necesito para mi app
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # Acá agrego las blueprints, que va a ser donde defina mis routes y mi error_handler.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app