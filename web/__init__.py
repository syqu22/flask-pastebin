from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import secrets

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    #Config of app
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///db/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from web.blueprints import views
    from web.blueprints import auth
    from web.blueprints import user_view

    #Register urls
    app.register_blueprint(views.views, url_prefix="/")
    app.register_blueprint(auth.auth, url_prefix="/")
    app.register_blueprint(user_view.user_view, url_prefix="/")

    from .models import User, Pastebin

    create_database(app)
    #Set up login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("web/db/" + DB_NAME):
        db.create_all(app=app)
