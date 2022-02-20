import ip
from serverlogger import log
import sendmail
import settings
import file_handler
import socket
import tqdm
import os

# get device local ip
IP = ip.get_ip()
public_ip = "31.217.18.151"

# device's IP address
SERVER_HOST = "192.168.8.157"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Server is listening as {SERVER_HOST} at port {SERVER_PORT}")
log(f"[*] Server is listening as {SERVER_HOST} at port {SERVER_PORT}")

# accept connection if there is any
client_socket, address = s.accept()
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")
log(f"[+] {address} is connected.")

# create a folder with a hostname of a client
file_handler.create_folder('TEST')

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)


# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(
    filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
        if settings.sendAlerts:
            sendmail.send_alert('SecretTransfer - file transfer',
                                'File transfer has finished', 'work@kristijan.me')

# close the client socket
client_socket.close()
# close the server socket
s.close()
