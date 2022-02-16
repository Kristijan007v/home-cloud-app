from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import base64

keyPair = RSA.generate(4096)

def create_public_key():
    email = 'kiki.vidovic.6969@gmail.com'
    pubKey = keyPair.publickey()
    pubKeyPEM = pubKey.exportKey()
    save_to = f"static/Cloud/{email}/Settings/public-{email}.pem"
    with open(save_to, "wb") as key_file:
        key_file.write(pubKeyPEM)


def load_pub_key(email):
    
    #Loads the key from the current directory named `key.key`
    load_from = f"static/Cloud/{email}/Settings/public-{email}.pem"
    pubKey = RSA.importKey(open(load_from,'r').read())
    return pubKey


def load_priv_key(email):
    
    #Loads the key from the current directory named `key.key`
    load_from = f"static/Cloud/{email}/Settings/private-{email}.pem"
    privKey = RSA.importKey(open(load_from,'r').read())
    return privKey



def create_private_key():
    email = 'kiki.vidovic.6969@gmail.com'
    privKeyPEM = keyPair.exportKey()
    save_to = f"static/Cloud/{email}/Settings/private-{email}.pem"
    with open(save_to, "wb") as key_file:
        key_file.write(privKeyPEM)



def encrypt(filename, pubKey):
    email = 'kiki.vidovic.6969@gmail.com'
    file_to_encrypt = open(filename, "rb").encode()
    encryptor = PKCS1_OAEP.new(pubKey)
    encrypted_file = encryptor.encrypt(file_to_encrypt)
    file = encrypted_file.binascii.hexlify
    save_to = f"static/Cloud/{email}/Settings/private-{email}.pem"
    with open(filename, "wb") as file:
        file.write(file)


def decrypt(filename):
    file_to_decrypt = open(filename, "rb").read()
    decryptor = PKCS1_OAEP.new(keyPair)
    decrypted_file = decryptor.decrypt(file_to_decrypt)
    with open(filename, "wb") as file:
        file.write(decrypted_file)

#create_public_key()
#create_private_key()

email = 'kiki.vidovic.6969@gmail.com'
pubKey = load_pub_key(email)
#privKey = load_priv_key(email)
filename = f"static/Cloud/test.txt"
encrypt(filename, pubKey)
#decrypt(filename, privKey)