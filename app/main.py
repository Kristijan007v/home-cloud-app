from http.cookiejar import MozillaCookieJar
from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from . import db
import os

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

@main.route('/my-cloud')
@login_required
def load_cloud():

    email = session['email']

    #Load and render all the files from the server for the current user
    basepath = f"static/Cloud/{email}/documents"
    dir = os.walk(basepath)
    file_list = []
    filename_list = []
    for path, subdirs, files in dir:
        for file in files:
            temp = os.path.join(path + '/', file)
            filename_list.append(file)
            file_list.append(temp)


    #Load and render all the images from the server for the current user
    basepath_images = f"static/Cloud/{email}/images"
    dir_images = os.walk(basepath_images)
    images_list = []
    image_names_list = []
    for path, subdirs, images in dir_images:
        for image in images:
            temp_images = os.path.join(path + '/', image)
            image_names_list.append(image)
            images_list.append(temp_images)
    return render_template('my-cloud.html', files=file_list, filenames = filename_list, hists = images_list)


