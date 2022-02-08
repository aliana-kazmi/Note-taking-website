from sqlalchemy import true
from . import db
from flask_login import UserMixin
from sqlalchemy import func
#schemas for the various functions it is going to perform
class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.String(18), db.ForeignKey('user.user_id'))


class User(db.Model, UserMixin):
    user_id = db.Column(db.String(18), primary_key = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(20))
    firstName = db.Column(db.String(20))
    notes = db.relationship('Note')
    #since the primary key has been named redundantly,
    #get_id() of login_user is to be overriden
    def get_id(self):
           return (self.user_id)
