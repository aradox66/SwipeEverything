"""Main Flask app."""

from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()
db = SQLAlchemy()
mail = Mail()

def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    mail.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.swipes import bp as swipes_bp
    app.register_blueprint(swipes_bp)

    from app import models

    return app
