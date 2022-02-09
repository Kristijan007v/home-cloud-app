from email import message
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from pathlib import Path
from . import db
import os
import glob

cloud = Blueprint('cloud', __name__)


#Create a folder with a requested name on the server
@cloud.route('/create-folder', methods=['POST'])
@login_required
def create_folder():
    # get all the data from the form 
    email = session['email']
    fname= request.form.get('folder_name')
    path = f"static/Cloud/{email}/Folders/{fname}"


    #Create given folder 
    create_folder = Path(f"static/Cloud/{email}/Folders/{fname}").mkdir(parents=True, exist_ok=True)

    if  create_folder != True:
        Path(f"static/Cloud/{email}/Folders/{fname}/documents").mkdir(parents=True, exist_ok=True)
        Path(f"static/Cloud/{email}/Folders/{fname}/images").mkdir(parents=True, exist_ok=True)
        Path(f"static/Cloud/{email}/Folders/{fname}/Folders").mkdir(parents=True, exist_ok=True)
        flash('Folder was created succesfully!')

    else:
        flash('Cannot create requested folder. Folder already exists.')

    return redirect(url_for('main.index'))


#Load all data from the requested folder
@cloud.route('/<folder>')
@login_required
def load_folder(folder):
    email = session['email']

    folder_link = f"/my-cloud/{folder}"

    #Load and render all the files from the server for the current user
    basepath = f"static/Cloud/{email}/Folders/{folder}/documents"
    dir = os.walk(basepath)
    file_list = []
    filename_list = []
    subdir_list = []
    files_number = 0
    for path, subdirs, files in dir:
        for file in files:
            temp = os.path.join(path + '/', file)
            filename_list.append(file)
            subdir_list.append(subdirs)
            file_list.append(temp)
            files_number += 1


    #Load and render all the folders from the server for the current user
    dirname = f"static/Cloud/{email}/Folders/{folder}/Folders"
    dir_folders = os.scandir(dirname)
    subfolders = glob.glob(dirname).sort()
    

    #Load and render all the images from the server for the current user
    basepath_images = f"static/Cloud/{email}/Folders/{folder}/images"
    dir_images = os.walk(basepath_images)
    images_list = []
    image_names_list = []
    images_number = 0
    for path, subdirs, images in dir_images:
        for image in images:
            temp_images = os.path.join(path + '/', image)
            image_names_list.append(image)
            images_list.append(temp_images)
            images_number += 1

    return render_template('folder.html', files=zip(file_list, filename_list), hists = zip(images_list, image_names_list), subfolders = subfolders, folder_link = folder_link, folder = folder, images_number = images_number, files_number = files_number )