from web import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    pastebins = db.relationship("Pastebin")

    def check_password(self, password):
        return check_password_hash(self.password, password)
