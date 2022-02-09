import os

MYDIR = f"D:/Github/home-cloud-app/app/static/Cloud/vidovic@kristijan.me/images"

folder_names = []
for entry_name in os.listdir(MYDIR):
    entry_path = os.path.join(MYDIR, entry_name)
    if os.path.isdir(entry_path):
        folder_names.append(entry_name)

print (folder_names)