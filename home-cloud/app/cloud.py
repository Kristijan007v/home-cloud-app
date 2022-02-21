from genericpath import exists
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, send_file, send_from_directory, Markup
from flask_login import login_required
from logger import txt_to_pdf, txt_to, load_json
from pathlib import Path
from models import db
import json
from classes import File
import os
from signature import digital_signature
import shutil


cloud = Blueprint('cloud', __name__)


@cloud.context_processor
def pass_folder():

    email = session['email']

    return dict(email=email)


# Create a folder with a requested name on the server
@cloud.route('/create-folder', methods=['POST'])
@login_required
def create_folder():

    # get all the data from the form
    email = session['email']
    fname = request.form.get('folder_name')
    path = f"static/Cloud/{email}/Folders/{fname}"

    # Create given folder
    create_folder = Path(
        f"static/Cloud/{email}/Folders/{fname}").mkdir(parents=True, exist_ok=True)

    if create_folder != True:
        Path(
            f"static/Cloud/{email}/Folders/{fname}/documents").mkdir(parents=True, exist_ok=True)
        Path(
            f"static/Cloud/{email}/Folders/{fname}/images").mkdir(parents=True, exist_ok=True)
        Path(
            f"static/Cloud/{email}/Folders/{fname}/Folders").mkdir(parents=True, exist_ok=True)
        flash('Folder was created succesfully!')

    else:
        flash('Cannot create requested folder. Folder already exists.')

    return redirect(url_for('main.index'))


# Load all data from the requested folder
@cloud.route('/<folder>')
@login_required
def load_folder(folder):

    email = session['email']
    folder_link = f"/my-cloud/{folder}"
    user_route = request.path

    # Load and render all the files from the server for the current user
    basepath = f"static/Cloud/{email}/Folders/{folder}/documents"
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

    # Load and render all the images from the server for the current user
    basepath_images = f"static/Cloud/{email}/Folders/{folder}/images"
    dir_images = os.walk(basepath_images)
    images_list = []
    image_names_list = []
    images_number = 0
    for path, subdirs, images in dir_images:
        for image in images:
            if not image.endswith('.json'):
                temp_images = os.path.join(path + '/', image)
                image_names_list.append(image)
                images_list.append(temp_images)
                images_number += 1

    return render_template('folder.html', files=zip(file_list, filename_list),
                           hists=zip(images_list, image_names_list), folder_link=folder_link, folder=folder, images_number=images_number,
                           files_number=files_number, user_route=user_route)


# Generate a pdf login report from the saved logs upon user request
@cloud.route('/generate-report')
def generate_pdf():

    email = session['email']
    logName = f"{email}-login-logs.txt"
    extension = 'rtf'
    txt_to_pdf(logName)
    txt_to(extension, logName)

    return redirect(url_for('cloud.load_folder', folder='Reports'))


# Show image info from JSON
@cloud.route('/info/<image_name>')
def image_info(image_name):

    email = session['email']
    file_name, file_size, ext, created_at = load_json(email, image_name)

    return render_template('image-info.html',
                           image_name=image_name, file_name=file_name, file_size=file_size, ext=ext, created_at=created_at)

# Show image info from XML


@cloud.route('/edit-info/<image_name>')
def edit_image_info(image_name):

    email = session['email']
    file_name, file_size, ext, created_at = load_json(email, image_name)

    return render_template('edit-image-info.html',
                           image_name=image_name, file_name=file_name, file_size=file_size, ext=ext, created_at=created_at)

# Rename images


@cloud.route('/rename/<image_name>', methods=['POST'])
def image_rename(image_name):

    email = session['email']
    new_name = request.form.get('new_name')
    image_path = f"static/Cloud/{email}/images/{image_name}"
    image_path_new = f"static/Cloud/{email}/images/{new_name}"
    os.rename(image_path, image_path_new)

    json_path = f"static/Cloud/{email}/images/{image_name}.json"
    json_path_new = f"static/Cloud/{email}/images/{new_name}.json"
    os.rename(json_path, json_path_new)

    a_file = open(json_path_new, "r")
    json_object = json.load(a_file)
    json_object["file_name"] = new_name

    a_file = open(json_path_new, "w")
    json.dump(json_object, a_file)
    a_file.close()

    flash("Image was renamed succesfully!")
    return redirect(url_for('main.index'))


@cloud.route('/file-info/<filename>/<foldername>')
def file_info(filename, foldername):

    email = session['email']
    file = f"static/Cloud/{email}/documents/{filename}"

    if foldername == "no":
        base_path = f"static/Cloud/{email}/documents/"
        folder = False
    else:
        base_path = f"static/Cloud/{email}/Folders/{foldername}/documents/"
        file = f"{base_path}/{filename}"
        folder = True

    xml_check = f"{base_path}/{filename}.xml"

    if exists(xml_check):
        file_name, file_size, created_at, signature = File.load_info(
            email, base_path, filename, 0, get_all=True)

        check_signature = digital_signature(file)

        if signature != check_signature:
            status = True
        else:
            status = False

        return render_template('file-info.html', filename=filename, file_name=file_name,
                               file_size=file_size, created_at=created_at, signature=signature, status=status,
                               folder=folder, foldername=foldername)
    else:
        flash("XML info file does not exist!")
        return redirect(url_for('main.index'))


@cloud.route('/edit-file-info/<filename>/<foldername>')
def edit_file_info(filename, foldername):

    email = session['email']

    if foldername == "no":
        base_path = f"static/Cloud/{email}/documents/"
        file_name, file_size, created_at, signature = File.load_info(
            email, base_path, filename, 0, get_all=True)

        return render_template('edit-file-info.html', filename=filename, file_name=file_name,
                               file_size=file_size, created_at=created_at)
    else:
        base_path = f"static/Cloud/{email}/Folders/{foldername}/documents/"
        file = f"{base_path}/{filename}"
        file_name, file_size, created_at, signature = File.load_info(
            email, base_path, filename, 0, get_all=True)

        return render_template('edit-file-info-folder.html', filename=filename, file_name=file_name,
                               file_size=file_size, created_at=created_at)


@cloud.route('/file-rename/<filename>', methods=['POST'])
def file_rename(filename):

    email = session['email']
    new_name = request.form.get('new_name')
    file_path = f"static/Cloud/{email}/documents/{filename}"
    file_path_new = f"static/Cloud/{email}/documents/{new_name}"
    os.rename(file_path, file_path_new)

    xml_path = f"static/Cloud/{email}/documents/{filename}.xml"
    xml_path_new = f"static/Cloud/{email}/documents/{new_name}.xml"
    os.rename(xml_path, xml_path_new)

    #File.update_info(filename, new_name)

    flash("File was renamed succesfully!")
    return redirect(url_for('main.index'))


@cloud.route('/download-file/<filename>/<foldername>')
def download_file(filename, foldername):

    email = session['email']
    file = f"static/Cloud/{email}/documents/{filename}"

    if foldername == "no":
        base_path = f"static/Cloud/{email}/documents/"
        directory = f"static/Cloud/{email}/documents"
        file = f"static/Cloud/{email}/documents/{filename}"
    else:
        base_path = f"static/Cloud/{email}/Folders/{foldername}/documents"
        directory = f"static/Cloud/{email}/Folders/{foldername}/documents"
        file = f"{base_path}/{filename}"

    # Get original file signature than compare it to the current one to check if the file was tampared with
    orginal_signature = File.load_info(
        email, base_path, filename, 3, get_all=False)
    check_signature = digital_signature(file)

    if orginal_signature != check_signature:
        flash(Markup(
            f"Your file was tampered with, beware! <a style='text-decoration:underline;' href='{file}' download='{file}'>Click here to download</a>"))
        return redirect(url_for('main.index'))
    else:
        return send_from_directory(directory, filename, as_attachment=True)
