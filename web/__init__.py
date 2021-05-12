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
    from web.models import User, Pastebin

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

    from web import pastebin
    from web import auth
    from web import user
    from web import public_pastebins
    from web import errors

    #Register urls
    app.register_blueprint(pastebin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(public_pastebins.bp)
    app.register_blueprint(errors.bp)

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
