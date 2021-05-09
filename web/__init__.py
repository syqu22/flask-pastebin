from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from os import path
from flask_login import LoginManager
import secrets

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    from web.models.user import User
    from web.models.pastebin import Pastebin

    app = Flask(__name__)
    #Config of the flask app
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///db/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = "yeti"

    #Create admin
    admin = Admin(app, template_mode='bootstrap4')

    #Add models to admin view
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Pastebin, db.session))

    db.init_app(app)

    from web.blueprints import pastebin_view
    from web.blueprints import auth_view
    from web.blueprints import user_view
    from web.blueprints import error_view

    #Register urls
    app.register_blueprint(pastebin_view.pastebin_view, url_prefix="/")
    app.register_blueprint(auth_view.auth_view, url_prefix="/")
    app.register_blueprint(user_view.user_view, url_prefix="/")
    app.register_blueprint(error_view.error_view, url_prefix="/")

    create_database(app)
    
    #Set up login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth_view.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("web/db/" + DB_NAME):
        db.create_all(app=app)
        db.session.execute("SELECT * FROM user")
