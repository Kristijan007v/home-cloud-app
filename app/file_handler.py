import settings
import pathlib
import time
from datetime import datetime, timezone

# GET CURRENT DATE
time_now = datetime.now()
write_date = time_now.strftime('%a %b %d %Y')


def create_folder(client):
    # create a folder with a hostname of a client
    """ folder_name = socket.gethostbyaddr(address) """
    client_name = '/' + client + '/'
    default_destination = settings.output_destination
    output_destination = default_destination + client_name + write_date
    pathlib.Path(output_destination).mkdir(parents=True, exist_ok=True)
