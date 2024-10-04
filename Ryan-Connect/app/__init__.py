from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    if app.config['ENV'] == 'development':
        app.config['DEBUG'] = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main
    app.register_blueprint(main)

    # Register toisoformat filter
    from .utils import toisoformat
    app.jinja_env.filters['toisoformat'] = toisoformat

    return app