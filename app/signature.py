import hashlib


def digital_signature(upload_path):

    md5_hash = hashlib.md5()

    a_file = open(upload_path, "rb")
    content = a_file.read()
    md5_hash.update(content)

    digest = md5_hash.hexdigest()

    return digest


#upload_path = "static/Cloud/kiki.vidovic.6969@gmail.com/documents/test2.txt"
#signature = digital_signature(upload_path)
# print(signature)
