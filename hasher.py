import hashlib


def hash(secret, random_code):
    txt = secret + ":" + random_code
    return hashlib.sha512(str.encode(txt)).hexdigest()
