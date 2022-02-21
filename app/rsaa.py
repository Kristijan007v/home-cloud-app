from Crypto import Cipher
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


rsa_pub = "static/Cloud/Security/public.pem"
rsa_priv = "static/Cloud/Security/private.pem"


def generate_keys():
    # privKEY,pubKey
    private_key = RSA.generate(2048)  # shortened for testing
    public_key = private_key.publickey()
    # 'convert' really store
    with open(rsa_priv, 'w') as pr:
        pr.write(private_key.exportKey().decode())
    with open(rsa_pub, 'w') as pu:
        pu.write(public_key.exportKey().decode())


def rsa_encrypt(email):
    # encrypt
    aes_key = f"static/Cloud/{email}/Settings/{email}.key"
    key = open(aes_key, 'r').read()
    message = key.encode()
    pu_key = RSA.importKey(open(rsa_pub, 'r').read())
    ciphertext = PKCS1_OAEP.new(pu_key).encrypt(message)
    with open(aes_key, 'wb') as f:
        f.write(ciphertext)


def rsa_decrypt(email):
    # decrypt
    aes_key = f"static/Cloud/{email}/Settings/{email}.key"
    ciphertext = open(aes_key, 'rb').read()
    pr_key = RSA.importKey(open(rsa_priv, 'r').read())
    decrypted = PKCS1_OAEP.new(pr_key).decrypt(ciphertext)
    with open(aes_key, 'wb') as f:
        f.write(decrypted)


#email = 'kiki.vidovic.6969@gmail.com'
# generate_keys()
# rsa_encrypt('kiki.vidovic.6969@gmail.com')
# decrypt(email)
# Test passed
