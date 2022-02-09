from http.cookiejar import MozillaCookieJar
from flask import Blueprint, render_template, session, request, jsonify, flash
from flask_login import login_required, current_user
from . import db
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

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
def index():

    email = session['email']

    #Load and render all the files from the server for the current user
    basepath = f"static/Cloud/{email}/documents"
    dir = os.walk(basepath)
    file_list = []
    filename_list = []
    subdir_list = []
    for path, subdirs, files in dir:
        for file in files:
            temp = os.path.join(path + '/', file)
            filename_list.append(file)
            subdir_list.append(subdirs)
            file_list.append(temp)


    #Load and render all the folders from the server for the current user




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
    return render_template('index.html', files=zip(file_list, filename_list), hists = zip(images_list, image_names_list))

#Allowed file types for upload
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




#File upload API route
@main.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	#check if there is file selected for upload
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	#upload file to the server
	if file:
		filename = secure_filename(file.filename)
		file.save(os.path.join(f"static/Cloud/vidovic@kristijan.me/images", filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	#Handle unallowed file types
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

