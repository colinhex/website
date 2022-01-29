from passlib.hash import sha256_crypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import urlsafe_b64decode, urlsafe_b64encode
from flask import url_for


def str_un_pad(string):
    return string[0:-int(string[-1])]


def str_pad(string, block_size):
    n = block_size - (len(string) % block_size)
    for i in range(1, n):
        string += '0'
    string += str(n)
    return string


def encrypt_data(data: str, secret: bytes):
    padded_data = str_pad(data, 4)
    data_b = urlsafe_b64decode(padded_data)
    cipher = AES.new(secret, AES.MODE_CBC)
    data_encrypted = cipher.encrypt(pad(data_b, AES.block_size))
    return urlsafe_b64encode(b''.join([data_encrypted, cipher.iv])).decode('ascii')


def decrypt_data(data: str, secret: bytes):
    data_b = urlsafe_b64decode(data)
    cipher = AES.new(secret, AES.MODE_CBC, iv=data_b[-AES.block_size::])
    data_decrypted = unpad(cipher.decrypt(data_b[0:-AES.block_size]), AES.block_size)
    return str_un_pad(urlsafe_b64encode(data_decrypted).decode('ascii'))


def hash_password(password: str):
    return sha256_crypt.hash(password)


def verify_password(password_hash, password: str):
    return sha256_crypt.verify(secret=password, hash=password_hash)


def is_safe_redirect(redirect_url, app):
    links = []
    with app.app_context(),  app.test_request_context():
        for rule in app.url_map.iter_rules():
            defaults = rule.defaults if rule.defaults is not None else ()
            arguments = rule.arguments if rule.arguments is not None else ()
            if "GET" in rule.methods and len(defaults) >= len(arguments):
                links.append(url_for(rule.endpoint, **(rule.defaults or {})))
    return redirect_url in links

