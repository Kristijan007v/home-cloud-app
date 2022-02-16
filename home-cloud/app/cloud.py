from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required
from logger import txt_to_pdf, txt_to
from pathlib import Path
from models import db
import os


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
    user_route = request.path

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

    return render_template('folder.html', files=zip(file_list, filename_list), 
    hists = zip(images_list, image_names_list), folder_link = folder_link, folder = folder, images_number = images_number, 
    files_number = files_number, user_route = user_route )


#Generate a pdf login report from the saved logs upon user request 
@cloud.route('/generate-report')
def generate_pdf():
    
    email = session['email']
    logName = f"{email}-login-logs.txt"
    extension = 'rtf'
    txt_to_pdf(logName)
    txt_to(extension, logName)

    return redirect(url_for('cloud.load_folder', folder = 'Reports'))