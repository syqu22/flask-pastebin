from flask import flash
from web import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from dateutil.relativedelta import relativedelta
import uuid 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    pastebins = db.relationship("Pastebin")

    def __repr__(self):
        return f"User: {self.id}, username: {self.username}, email={self.email}"

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

    def to_dict(self):
        """
        Generate a new dict/object based on user data
        """
        data = {
            "id": self.id,
            "_username": self.username,
        }
        
        return data

class Pastebin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default="Untitled")
    content = db.Column(db.String(60000))
    syntax = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True))
    expire_date = db.Column(db.DateTime(timezone=True))
    password = db.Column(db.String(150))
    link = db.Column(db.String(150), unique=True) 

    def __init__(self, title: str, content: str, syntax: str, user_id: id, expire_date: str, password: str):
        self.title = title
        self.content = content
        self.syntax = syntax
        self.user_id = user_id
        self.date = datetime.utcnow().replace(microsecond=0)
        self.expire_date = self.format_expire_date(expire_date)
        self.link = str(uuid.uuid4())[:8]
        if password:
            self.set_password(password)

    def __repr__(self):
        return f"Pastebin {self.id}, title: {self.title}, syntax: {self.syntax}, user_id: {self.user_id}, date: {self.date}, expire_date {self.expire_date}"

    def is_expired(self):
        """
        Check if the pastebin date has expired
        if so delete it from database and return True
        """
        if self.expire_date:
            if datetime.utcnow() > self.expire_date:
                db.session.delete(self)
                db.session.commit()
                return True
            return False
        else:
            return False
    
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

    def format_expire_date(self, date: str):
        """
        Return the date + difference between expiration date
        as long as input date is valid
        """
        dates = {
            "test":  self.date,
            "1 minute":  self.date + relativedelta(minutes=+1),
            "15 minutes": self.date + relativedelta(minutes=+15),
            "1 hour":  self.date + relativedelta(hours=+1),
            "1 day":   self.date + relativedelta(days=+1),
            "1 week":  self.date + relativedelta(weeks=+1),
            "1 month": self.date + relativedelta(months=+1),
            "1 year":  self.date + relativedelta(years=+1)
        }

        if date in dates:
            return dates.get(date)
        else:
            return None

    def to_dict(self):
        """
        Generate a new dict/object based on user data
        """
        if not self.is_expired():
            if not self.password:
                data = {
                    "id": self.id,
                    "_title": self.title,
                    "content": self.content,
                    "syntax": self.syntax,
                    "date": self.date,
                    "expire_date": self.expire_date,
                    "link": self.link
                }
                return data
            else:
                return {
                    "id": self.id,
                    "password": "private",
                    "link": self.link,
                    }
