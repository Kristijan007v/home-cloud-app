from flask_login import UserMixin
from . import db

#User class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

#File class
class File(db.Model):
    fileId = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    fileName = db.Column(db.String(100), unique=True)
    createdAt = db.Column(db.String(100))
    fileSize = db.Column(db.String(100))
    owner = db.Column(db.String(1000))
