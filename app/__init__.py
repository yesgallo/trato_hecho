from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

# Crear una instancia de LoginManager
login_manager = LoginManager()

def create_app():
    # Crear una instancia de la aplicación Flask
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Inicializar la extensión SQLAlchemy
    db.init_app(app)

    # Configuración de Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Registrar los modelos
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar Blueprints
    from .views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from ..game import game as game_blueprint
    app.register_blueprint(game_blueprint)

    return app
