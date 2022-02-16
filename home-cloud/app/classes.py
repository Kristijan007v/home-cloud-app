#Classes
from logger import save_json
import json
import datetime
from flask import session

class File:
    def __init__(self, name, size, extension, date ):
        self.name = name
        self.size = size
        self.extension = extension
        self.date = date
    
    def save_info(self):
        # Data to be written
        dictionary ={
            "file_name" : str(f"{file.name}"),
            "file_size" : str(f"{file.size}"),
            "file_exstension" : str(f"{file.extension}"),
            "created_at" : str(f"{file.date}")
        }
        
        # Serializing json 
        json_object = json.dumps(dictionary, indent = 4)
        upload_path = f"static/Cloud/Test"
        #Saving json file
        new_name = f"{file.name}.json"
        save_to = f"{upload_path}/{new_name}"
        with open(save_to, "w") as outfile:
            outfile.write(json_object)


file = File('Test.docx', '10 MB', '.docx', '10-02-2022')
file.save_info()


class Log:
    def __init__(self, time, location, user_ip, user_browser ):
        self.time = time
        self.location = location
        self.user_ip = user_ip
        self.user_browser = user_browser

    def log_user(location, user_ip, user_browser, logName):

        time_now = datetime.now()
        file_wt = time_now.strftime('%d%m%Y-%H_%M_%S')
        email = session['email']
        upload_path = f"static/Cloud/{email}/Logs"

        # Data to be written
        dictionary ={
            "time": str(f"{file_wt}"),
            "location" : str(f"{location}"),
            "user_ip" : str(f"{user_ip}"),
            "user_browser" : str(f"{user_browser}"),
        }
        
        # Serializing json 
        json_object = json.dumps(dictionary, indent = 4)
        
        #Saving json file
        new_name = f"{logName}.json"
        save_to = f"{upload_path}/{new_name}"
        with open(save_to, "a") as outfile:
            outfile.write(json_object)

        def encrypt_log():
            #RSA
            pass

        def decrypt_log():
            #RSA
            pass

