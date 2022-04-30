from hashlib import pbkdf2_hmac
from cryptography.fernet import Fernet
import bcrypt
from pbkdf2 import PBKDF2
import pyDes


def get_hashed_password_and_salt(plain_text_password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_text_password, salt)

def check_password(plain_text_password, hashed_password):
    return hashed_password == bcrypt.hashpw(plain_text_password, hashed_password[:29])

def generate_decrypt_key(plain_text_password, salt):
    return PBKDF2(plain_text_password, salt).read(16)

def encrypt_userpasswords_password(plain_text_password, key):
    return pyDes.triple_des(key).encrypt(plain_text_password, padmode=2)

def decrypt_userpassword_password(encryptedpassword, key):
    return pyDes.triple_des(key).decrypt(encryptedpassword, padmode = 2).decode()

