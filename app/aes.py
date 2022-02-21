from json import load
from cryptography.fernet import Fernet
import os

# Generate encryption key


def write_key(email):

    key = Fernet.generate_key()
    save_to = f"static/Cloud/{email}/Settings/{email}.key"
    with open(save_to, "wb") as key_file:
        key_file.write(key)


# Load encryption key
def load_key(email):

    # Loads the key from the current directory named `key.key`
    load_from = f"static/Cloud/{email}/Settings/{email}.key"
    return open(load_from, "rb").read()


# Encrypt given file
def encrypt(filename, key):

    # Given a filename (str) and key (bytes), it encrypts the file and write it

    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


# Decrypt given file
def decrypt(filename, key):

    # Given a filename (str) and key (bytes), it decrypts the file and write it

    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)


# Encrypt given folder
def encrypt_folder(email, foldername):
    basepath = f"static/Cloud/{email}/{foldername}/"
    key = load_key(email)
    for filename in os.listdir(basepath):
        file = os.path.join(basepath, filename)
        encrypt(file, key)


# Decrypt given folder
def decrypt_folder(email, foldername):
    basepath = f"static/Cloud/{email}/{foldername}/"
    key = load_key(email)
    for filename in os.listdir(basepath):
        file = os.path.join(basepath, filename)
        decrypt(file, key)


""" email = 'kiki.vidovic.6969@gmail.com'
#write_key(email)
decrypt_folder(email, 'images') """
