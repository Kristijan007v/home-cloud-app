import time
from datetime import datetime, timezone
# Used to writing logs to "logs.txt" file

time_now = datetime.now()
write_date = time_now.strftime('%a %b %d')
write_time = time_now.strftime('%a %b %d %Y %H:%M:%S ')


def log(operation):

    f = open("logs.txt", "a")
    f.write("\n")
    f.write(write_time)
    f.write(operation)
    f.close()


log(" - Connecting to db")

\
