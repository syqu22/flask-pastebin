from web import db
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash

class Pastebin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), default="Untitled")
    content = db.Column(db.String(6000000))
    link = db.Column(db.String(150), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    expire_date = db.Column(db.DateTime(timezone=True))
    password = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    #Check if pastebin date expired, if so delete it from database
    def is_expired(self):
        if self.expire_date is not None:
            if datetime.utcnow() > self.expire_date:
                db.session.delete(self)
                db.session.commit()
                return True
            else:
                return False
        else:
            return False
    
    #Check if password is correct
    def check_password(self, password):
        return check_password_hash(self.password, password)

    #Encode link using base36
    def encode_link(self):
        link = self.id
        if link == 0:
            return "0"
        base36 = []
        while link != 0:
            link, i = divmod(link, 36)
            base36.append("0123456789abcdefghijklmnopqrstuvwxyz"[i])
            self.link = "".join(reversed(base36))
