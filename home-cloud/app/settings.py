import pathlib
import yaml

with open("config.yaml", "r") as cf:
    try:
        config = yaml.safe_load(cf)
    except yaml.YAMLError as exc:
        print(exc)

# Saving email settings to variables
smtp = config["email"]["smtp"]
port = config["email"]["port"]
account = config["email"]["account"]
password = config["email"]["password"]
testEmail = config["email"]["test-mail"]["email-address"]

# Advanced settings
checkTime = config["script-settings"]["check-time"]
urlFile = config["script-settings"]["url-file"]
timezone = config["script-settings"]["timezone"]
sendAlerts = config["script-settings"]["send-alerts"]
dev = config["script-settings"]["dev"]

if dev == 'yes':
    print(testEmail)
    print("Config file is loaded successfully...")


""" with open("crawler-config.yaml", "r") as crf:
    try:
        crawler = yaml.safe_load(crf)
    except yaml.YAMLError as cr_exc:
        print(cr_exc)

url = ["organization"][0]["urls"]

if dev == 'yes':
    for k in url:
        print(k)
    print("Crawler config file is loaded successfully...") """

# Creating output folder
output_destination = config["output"]["destination"]
pathlib.Path(output_destination).mkdir(parents=True, exist_ok=True)
