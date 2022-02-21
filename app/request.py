import requests
from requests.exceptions import HTTPError
import json
import time

def fetch_weather():
    try:
        response = requests.get('http://127.0.0.1:8080/weather/Zagreb')
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        upload_path = f"static/Cloud/Weather/"
        
        json_object = json.dumps(jsonResponse, indent = 4)
        #Saving json file
        new_name = f"weather.json"
        save_to = f"{upload_path}/{new_name}"
        with open(save_to, "w") as outfile:
            outfile.write(json_object)



    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


while True:
    fetch_weather()
    time.sleep(10)

