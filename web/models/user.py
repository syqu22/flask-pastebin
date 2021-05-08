from web.blueprints.user_view import user
from web import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    pastebins = db.relationship("Pastebin")

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method="sha256")

    #Check if password is correct
    def check_password(self, password: str):
        return check_password_hash(self.password, password)
