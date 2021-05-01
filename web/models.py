from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Pastebin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(6000000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    pastebins = db.relationship("Pastebin")