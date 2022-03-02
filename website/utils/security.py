from passlib.hash import sha256_crypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import url_for

# import logging
import re

# --------- Logging ----------
# logger = logging.getLogger('Security')

# ---------- Preferences ----------
__preferences: dict = {}


def set_pref(preferences):
    global __preferences
    __preferences = preferences


# ------------------------------------------------------------
#                       Security Module
# ------------------------------------------------------------

# --------------- General Encryption For Data -----------------

def encrypt_data(data: str) -> bytes:
    cipher = AES.new(
        pad(__preferences['SECRET_KEY'].encode('ascii'), AES.block_size),
        AES.MODE_CBC
    )

    data = data.encode('latin-1')
    data = cipher.encrypt(pad(data, AES.block_size))
    data = b''.join([data, cipher.iv])
    return data


def decrypt_data(data: bytes) -> str:
    cipher = AES.new(
        pad(__preferences['SECRET_KEY'].encode('ascii'), AES.block_size),
        AES.MODE_CBC,
        iv=data[-AES.block_size::]
    )

    data = unpad(cipher.decrypt(data[0:-AES.block_size]), AES.block_size)
    data = data.decode('latin-1')
    return data


# -------- Hash Passwords -------------

def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return sha256_crypt.verify(secret=password, hash=password_hash)


# ------- Verify Site Redirects ------------

def is_safe_redirect(redirect_url, app) -> bool:
    links = []
    with app.app_context(),  app.test_request_context():
        for rule in app.url_map.iter_rules():
            defaults = rule.defaults if rule.defaults is not None else ()
            arguments = rule.arguments if rule.arguments is not None else ()
            if "GET" in rule.methods and len(defaults) >= len(arguments):
                links.append(url_for(rule.endpoint, **(rule.defaults or {})))
    return redirect_url in links


# ------- User Activation Tokens -----------

def generate_verification_token(email) -> str:
    serializer = URLSafeTimedSerializer(secret_key=__preferences['SECRET_KEY'])
    return serializer.dumps(email, salt='verify')


def confirm_verification_token(token, expiration=3600) -> str:
    serializer = URLSafeTimedSerializer(secret_key=__preferences['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='verify',
            max_age=expiration
        )
    except SignatureExpired:
        raise ValueError('Illegitimate token, Expired')
    except BadSignature:
        raise ValueError('Illegitimate token, Bad Signature')
    return email


# -------- String Format Exploit Prevention & SQL Injections ------

def verify_email_pattern(email) -> bool:
    #  https://stackoverflow.com/a/201378
    pattern = r"?:[a-z0-9!  # $%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-" \
              r"\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])" \
              r"?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:" \
              r"(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-" \
              r"\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(pattern, email) is not None


def verify_alphanumerical_pattern(text) -> bool:
    pattern = r"^[a-zA-Z0-9\s]*$"
    return re.match(pattern, text) is not None

