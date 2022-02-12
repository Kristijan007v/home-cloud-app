from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .logger import get_info
from . import db
import requests
import pathlib
import math
import glob
import os


main = Blueprint('main', __name__)


#Allowed file types for upload
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Converting bytes to other units
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i]), s


#Calcutate folder or file size of the given folder, file name
def folder_size(Folderpath):
    # assign size
    size = 0   
    # get size
    for path, dirs, files in os.walk(Folderpath):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
            size_mb, size_mb_int = convert_size(size)
            size_mb_str = str(size_mb)

    return size_mb_str, size_mb_int


def current_dir():
    current_dir = os.getcwd()
    return current_dir


#Track variables for usage in all templates - FOR DEBUG ONLY
@main.context_processor
def pass_info():

    ip_address, location = get_info()

    return dict(ip_address = ip_address, location = location)


@main.route('/alert-test')
def send_alerts():
    email = session['email']

    dir = f"static/Cloud/{email}"
    disk_used, disk_used_int = folder_size(dir)

    if disk_used_int > 200:
        subject = 'Your cloud storage is full'
        message = 'Ovo je test.'
        destination = 'kiki.vidovic.6969@gmail.com'

        request_url = f"http://127.0.0.1:5000//email"
        requests.get(request_url)
    return redirect(url_for('main.index'))
    

#Render a profile page
@main.route('/profile')
@login_required
def profile():

    email = session['email']

    dir = f"static/Cloud/{email}"
    disk_used, disk_used_int = folder_size(dir)

    return render_template('profile.html', name=current_user.name, email=current_user.email, 
    disk_used = disk_used, disk_used_int = int(disk_used_int))


#Render a main index page - my-cloud
@main.route('/my-cloud')
@login_required
def index():

    email = session['email']

    #Load and render all the files from the server for the current user
    basepath = f"static/Cloud/{email}/documents"
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
    dirname = f"static/Cloud/{email}/Folders/*"
    subfolders= [os.path.basename(x) for x in glob.glob(dirname)]

    #Load and render all the images from the server for the current user
    basepath_images = f"static/Cloud/{email}/images"
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

    return render_template('index.html', files=zip(file_list, filename_list), hists = zip(images_list, image_names_list), subfolders = subfolders,
     images_number = images_number, files_number = files_number)


#File upload API route
@main.route('/file-upload', methods=['POST'])
def upload_file():
    email = session['email']
    current = os.path.abspath(os.path.dirname(__file__))
    dir = f"{current}/static/Cloud/vidovic@kristijan.me"
    disk_used, disk_used_int = folder_size(dir)
    image_ex = '.jpg'
    if request.method == 'POST':
        if disk_used_int < 400:
            file = request.files['file']
            file_extension = pathlib.Path(file.filename).suffix
            if file_extension == image_ex:
                filename = secure_filename(file)
                upload_path = f"static/Cloud/{email}/images"
                file.save(os.path.join(upload_path, filename))
                flash("Image uploaded succesfully.")
            else:
                upload_path = f"static/Cloud/{email}/documents"
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_path, filename))
                flash("File uploaded succesfully.")
        else:
            flash("Your storage is full.")
    return redirect(url_for('main.index'))

