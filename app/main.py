from http.cookiejar import MozillaCookieJar
from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

""" @main.route('/sendmail')
@login_required
def sendmail():
    return render_template('send-email.html') """


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, email=current_user.email)


