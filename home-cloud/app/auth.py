import email
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from logger import get_info
from models import User, db
from pathlib import Path
from aes import *
import os
import shutil
from classes import Log


auth = Blueprint('auth', __name__)


# Render a login page
@auth.route('/login')
def login():
    return render_template('login.html')


# Render a signup page
@auth.route('/signup')
def signup():
    return render_template('signup.html')


# Render a reset-password page
@auth.route('/reset-password')
@login_required
def reset_password():
    return render_template('reset-password.html')


# Route to procces login request
@auth.route('/login', methods=['POST'])
def login_post():

    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Decrypt documents upon user login
    foldername = 'documents'
    decrypt_folder(email, foldername)

    User.login(email, password, remember)

    # get all the user data and save it to log file
    get_info()

    return redirect(url_for('main.index'))


# Route to procces signup request
@auth.route('/signup', methods=['POST'])
def signup_post():

    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    User.signup(email, name, password)

    # Generate AES ENCRYPTION KEY
    write_key(email)

    return redirect(url_for('auth.login'))


# Route to procces a password reset request
@auth.route('/reset-password', methods=['POST'])
@login_required
def reset_password_post():

    email = session['email']
    # get all the data from the form
    password = request.form.get('new-password')
    password_repeat = request.form.get('new-password-repeat')

    if password == password_repeat:

        # Get current signed in user
        user = User.query.filter_by(email=email).first()
        # generate a new password
        new_pasw = generate_password_hash(password, method='sha256')

        # commit new password to the db
        user.password = new_pasw
        db.session.commit()
    else:
        flash('Entered passwords are not the same')

    logout_user()
    return redirect(url_for('auth.login'))


# Route to procces a delete account request
@auth.route('/delete-account', methods=['POST'])
@login_required
def delete_account():

    email = session['email']
    email_form = request.form.get('delete-confirmation')

    if email == email_form:

        delete_folder = f"static/Cloud/{email}"

        # Delete user data from  db
        User.query.filter_by(email=email).delete()
        db.session.commit()

        # Delete user folder from server
        file_path = os.path.join(delete_folder)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            flash('Failed to delete your account')

        flash('Your account was succesfully deleted.')
        return redirect(url_for('auth.login'))

    flash('Wrong confirmation message typed in.')
    return redirect(url_for('main.profile'))


# Process a logout request
@auth.route('/logout')
@login_required
def logout():
    email = session['email']
    foldername = 'documents'
    # Encrypt documents before logout
    encrypt_folder(email, foldername)

    logout_user()
    return redirect(url_for('auth.login'))
