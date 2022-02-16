from enum import unique
from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask import request, flash, redirect, url_for, session
from sqlalchemy import false
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import datetime
from app import db



#User class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def login(email, password, remember):

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
         # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            success=False
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

        login_user(user, remember=remember)
        session['email'] = email
        success = True
    
    def signup(email, name, password):

        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        # if a user is found, we want to redirect back to signup page so user can try again
        if user: 
            flash('Email address already exists. Please login.')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        #Create all necesseary folders for the new user
        Path(f"static/Cloud/{email}/documents").mkdir(parents=True, exist_ok=True)
        Path(f"static/Cloud/{email}/images").mkdir(parents=True, exist_ok=True)
        Path(f"static/Cloud/{email}/Folders/Reports").mkdir(parents=True, exist_ok=True)
        Path(f"static/Cloud/{email}/Computers").mkdir(parents=True, exist_ok=True)
        Path(f"static/Cloud/{email}/Logs").mkdir(parents=True, exist_ok=True)
        Path(f"static/Cloud/{email}/Settings/settings.ini").mkdir(parents=True, exist_ok=True)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

class File(db.Model):
    fileId = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    fileName = db.Column(db.String(1000), unique=True)
    fileExt = db.Column(db.String(100))
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
