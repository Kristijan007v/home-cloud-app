from genericpath import exists
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from logger import get_info, save_json
from classes import File
from models import db
import json
import requests
from config import load_settings, save_settings, get_reg, set_reg
import pathlib
import time
import math
import glob
import os
import shutil
from signature import digital_signature


main = Blueprint('main', __name__)


# Allowed file types for upload
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Converting bytes to other units
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i]), s


# Calcutate folder or file size of the given folder, file name
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


# Track variables for usage in all templates - FOR DEBUG ONLY
@main.context_processor
def pass_info():

    ip_address, location = get_info()
    email = session['email']
    image_quality_str, image_quality, ip_info, show_folders = load_settings()
    logging_value = get_reg('LOG_DATA')
    show_images = get_reg('SHOW_IMAGES')
    show_files = get_reg('SHOW_FILES')

    return dict(ip_address=ip_address, location=location, email=email, image_quality=image_quality,
                image_quality_str=image_quality_str, ip_info=ip_info,
                show_folders=show_folders, logging_value=logging_value, show_images=show_images, show_files=show_files)


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

# Render index welcome page


@main.route('/')
@login_required
def welcome():
    weather_path = 'static/Cloud/Weather/weather.json'
    f = open(weather_path)
    parse_json = json.load(f)
    temp = parse_json['temperature']
    pressure = parse_json['pressure']
    humidity = parse_json['humidity']
    f.close()

    return render_template('welcome.html', temp=temp, pressure=pressure, humidity=humidity)


# Render a profile page
@main.route('/profile')
@login_required
def profile():

    email = session['email']

    dir = f"static/Cloud/{email}"
    disk_used, disk_used_int = folder_size(dir)

    return render_template('profile.html', name=current_user.name, email=current_user.email,
                           disk_used=disk_used, disk_used_int=int(disk_used_int))


# Render a main index page - my-cloud
@main.route('/my-cloud')
@login_required
def index():

    email = session['email']

    # Load and render all the files from the server for the current user
    basepath = f"static/Cloud/{email}/documents"
    dir = os.walk(basepath)
    file_list = []
    filename_list = []
    subdir_list = []
    files_number = 0
    for path, subdirs, files in dir:
        for file in files:
            if not file.endswith('.xml'):
                temp = os.path.join(path + '/', file)
                filename_list.append(file)
                subdir_list.append(subdirs)
                file_list.append(temp)
                files_number += 1

    # Load and render all the folders from the server for the current user
    dirname = f"static/Cloud/{email}/Folders/*"
    subfolders = [os.path.basename(x) for x in glob.glob(dirname)]

    # Load and render all the images from the server for the current user
    basepath_images = f"static/Cloud/{email}/images"
    dir_images = os.walk(basepath_images)
    images_list = []
    image_names_list = []
    images_number = 0
    for path, subdirs, images in dir_images:
        for image in images:
            if image.endswith(".jpeg") or image.endswith(".jpg"):
                temp_images = os.path.join(path + '/', image)
                image_names_list.append(image)
                images_list.append(temp_images)
                images_number += 1

    return render_template('index.html', files=zip(file_list, filename_list), hists=zip(images_list, image_names_list), subfolders=subfolders,
                           images_number=images_number, files_number=files_number)


@main.route('/sharenet')
def sharenet():
    return render_template('sharenet.html')


# File upload API route
@main.route('/file-upload', methods=['POST'])
def upload_file():
    email = session['email']
    current = os.path.abspath(os.path.dirname(__file__))
    dir = f"{current}/static/Cloud/{email}"
    if request.method == 'POST':
        file = request.files['file']
        upload_path = f"static/Cloud/{email}/documents"
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_path, filename))

        # Get all the file information
        file_size = convert_size(os.path.getsize(upload_path))
        created_at = time.ctime(os.path.getmtime(upload_path))
        file_extension = pathlib.Path(file.filename).suffix
        signature = digital_signature(f"{upload_path}/{filename}")
        file = File(filename, file_size, file_extension, created_at, signature)
        # Save file info to xml
        #File.save_info(file.name, file.size, file.extension, file.date)
        file.save_info(email)
        flash("File uploaded succesfully.")
    return redirect(url_for('main.index'))


# Upload images
@main.route('/upload-test/<email>', methods=['POST'])
def upload_test(email):

    file = request.files['file']

    filename = file.filename

    upload_path = f"static/Cloud/{email}/images"
    file.save(os.path.join(upload_path, filename))

    file_path = f"{upload_path}/{filename}"
    # Get all the file information
    file_size = convert_size(os.path.getsize(file_path))
    created_at = time.ctime(os.path.getmtime(file_path))
    file_extension = pathlib.Path(file.filename).suffix
    # Save to json
    save_json(filename, file_size, file_extension, created_at, upload_path)

    return ("Success!")


# Delete selected file from the server
@main.route('/delete-file/<filename>')
def delete_file(filename):
    email = session['email']
    location = f"static/Cloud/{email}/documents"
    path = os.path.join(location, filename)
    xml_path = os.path.join(location, f"{filename}.xml")

    if exists(xml_path):
        os.remove(path)
        os.remove(xml_path)
    else:
        os.remove(path)

    flash(f'File "{filename}" was deleted succesfully.')
    return redirect(url_for('main.index'))


# Delete selected image from the server
@main.route('/delete-image/<image_name>')
def delete_image(image_name):
    email = session['email']
    location = f"static/Cloud/{email}/images"
    json_location = f"static/Cloud/{email}/images/{image_name}.json"
    path = os.path.join(location, image_name)
    os.remove(path)
    os.remove(json_location)
    flash(f'Image "{image_name}" was deleted succesfully.')
    return redirect(url_for('main.index'))


# Delete selected folder from the server
@main.route('/delete-folder/<folder_name>')
def delete_folder(folder_name):

    email = session['email']
    delete_folder = f"static/Cloud/{email}/Folders/"

    # Delete user folder from server
    file_path = os.path.join(delete_folder, folder_name)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        flash('Failed to delete selected folder')

    flash(f'Folder "{folder_name}" deleted succesfully!')
    return redirect(url_for('main.index'))


# Save image quality settings
@main.route('/save-settings/<image_quality>')
def image_settings(image_quality):

    section = 'image'
    setting = 'upload_quality'
    save_settings(section, setting, image_quality)

    flash("Image upload settings were saved successfully!")
    return redirect(url_for('main.index'))


# Save ip banner info settings
@main.route('/save-ip-settings/<ip_setting>')
def ip_settings(ip_setting):

    section = 'layout'
    setting = 'ip_info'
    save_settings(section, setting, ip_setting)

    flash("IP layout settings were saved successfully!")
    return redirect(url_for('main.index'))


# Save show/hide folder setting.ini
@main.route('/save-folders-settings/<folders_settings>')
def folders_settings(folders_settings):

    section = 'layout'
    setting = 'show_folders'
    save_settings(section, setting, folders_settings)

    flash("Settings were saved successfully!")
    return redirect(url_for('main.index'))


# Turn logging on or off
@main.route('/manage-logging/<value>')
def logging(value):
    set_reg('LOG_DATA', value)
    flash("Logging settings were applied successfully!")
    return redirect(url_for('main.profile'))


# Search
@main.route('/search', methods=['POST'])
def search():
    term = request.form.get('term')

    if term == 'imhide':
        set_reg('SHOW_IMAGES', 'False')
        flash("Image section set to hide!")
    elif term == 'imshow':
        set_reg('SHOW_IMAGES', 'True')
        flash("Image section set to show!")
    elif term == 'fhide':
        set_reg('SHOW_FILES', 'False')
        flash("Files section set to hide!")
    elif term == 'fshow':
        set_reg('SHOW_FILES', 'True')
        flash("Files section set to show!")

    return redirect(url_for('main.index'))


@main.route('/downlaod/<filename>')
def download_file(filename):
    pass
