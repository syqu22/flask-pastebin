from web import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    pastebins = db.relationship("Pastebin")

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.set_password(password)

    def check_password(self, password: str):
        """
        Return true if given password is the same as pastebin's password
        """
        return check_password_hash(self.password, password)

    def set_password(self, password: str):
        """
        Generate a new password hash and set it for user
        """
        self.password = generate_password_hash(password, method="sha256")

    def is_valid(self, password1, password2):
        """
        Validate if user has correct data
        """
        if len(self.username) < 4:
            flash("Username must be greater than 3 characters.", category="error")
            return False
        if len(self.email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
            return False
        if len(password1) < 5:
            flash("Password must be at least 5 characters long.", category="error")
            return False
        if password1 != password2:
            flash("Passwords are not the same.", category="error")
            return False
        else:
            return True
