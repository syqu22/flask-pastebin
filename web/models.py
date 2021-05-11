from flask import flash
from web import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from dateutil.relativedelta import relativedelta
import uuid 

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

class Pastebin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), default="Untitled")
    content = db.Column(db.String(6000000))
    paste_type = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True))
    expire_date = db.Column(db.DateTime(timezone=True))
    password = db.Column(db.String(150))
    link = db.Column(db.String(150), unique=True) 

    def __init__(self, title: str, content: str, paste_type: str, user_id: id, expire_date: str, password: str):
        self.title = title
        self.content = content
        self.paste_type = paste_type
        self.user_id = user_id
        self.date = datetime.utcnow().replace(microsecond=0)
        self.expire_date = self.format_expire_date(expire_date)
        self.link = str(uuid.uuid4())[:8]
        if password:
            self.set_password(password)

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
            "1min":  self.date + relativedelta(minutes=+1),
            "15min": self.date + relativedelta(minutes=+15),
            "hour":  self.date + relativedelta(hours=+1),
            "day":   self.date + relativedelta(days=+1),
            "week":  self.date + relativedelta(weeks=+1),
            "month": self.date + relativedelta(months=+1),
            "year":  self.date + relativedelta(years=+1)
        }

        if date in dates:
            return dates.get(date)
        else:
            return None

    def is_valid(self):
        """
        Validate if pastebin has correct data
        """
        types = {
        "text", "bash", "c", "c#", "c++", "css", "go", "html", "http", "ini", "java", "js","json", "kotlin", 
        "lua", "markdown", "objectivec", "perl", "php", "python", "r", "ruby", "rust", "sql", "swift", "typescript",
        }

        if self.content:
            if self.title:
                if len(self.title) > 150:
                    flash("Title cannot exceed 150 characters limit.", category="error")
                    return False
            if len(self.content) > 6000000:
                flash("Your pastebin cannot exceed 6000000 characters limit.", category="error")
                return False
            if self.paste_type not in types:
                flash("The syntax type you have choosed does not exist.", category="error")
                return False
            else:
                return True
        else:
            flash("Your pastebin must be at least 1 character long.", category="error")
            return False
