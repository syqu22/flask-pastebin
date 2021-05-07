from web import db
from datetime import datetime
from sqlalchemy.sql import func

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
            if datetime.utcnow() > self.pastebin.expire_date:
                db.session.delete(self)
                db.session.commit()
                return False
            else:
                return True
        else:
            return True
