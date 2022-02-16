from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

keyPair = RSA.generate(3072)

pubKey = keyPair.publickey()
print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()
print(pubKeyPEM.decode('ascii'))

print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
privKeyPEM = keyPair.exportKey()
print(privKeyPEM.decode('ascii'))

email = 'kiki.vidovic.6969@gmail.com'
msg = b'kydWQfGg6cpA9p6SydpEA1DwsWi5CYoluq29QwBEcuk='
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(msg)
save_to = f"static/Cloud/{email}/Settings/aes.txt"
with open(save_to, "wb") as file:
    file.write(binascii.hexlify(encrypted))
print("Encrypted:", binascii.hexlify(encrypted))


save_to_de = f"static/Cloud/{email}/Settings/aes_de.txt"
with open(save_to) as f:
    lines = f.readlines()
decryptor = PKCS1_OAEP.new(keyPair)
decrypted = decryptor.decrypt(lines)
with open(save_to_de, "wb") as file:
    file.write(decrypted.decode())
print('Decrypted:', decrypted.decode())