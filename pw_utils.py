# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 17:16:35 2021

@author: Rob
"""
import PySimpleGUI as sg
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64


def getpw_1liner():
    
    event, values = sg.Window('Login Window', 
                             [[sg.T('Enter your passwrd'), sg.In(key='-ID-', password_char='*')],
                              [sg.B('OK'), sg.B('Cancel')]]).read(close=True)
    return values['-ID-']

def test_pwflow():
    (key, epw) = encryptpw(getpw_1liner())
    decryptpw(key, epw)
    
def encryptpw(pw):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    pwe = cipher.encrypt(pw.encode())
    return key, pwe

def decryptpw(key, epw):
    cipher = Fernet(key)
    pw = cipher.decrypt(epw).decode()
    return pw


def test_pw_with_pw():
    pw = 'powerlevel1000'
    msg = 'this is a secret message that cant be very long'
    emsg = encrypt_using_password(pw, msg)
    
    msg2 = decrypt_using_password(pw, emsg)
    assert msg == msg2

def encrypt_using_password(pw, msg):
    envsalt = os.getenv('salt16')
    salt = int.to_bytes(int(envsalt), 16, 'little') if envsalt else os.urandom(16)
    os.environ['salt16'] = str(int.from_bytes(salt, 'little'))
    kdf = PBKDF2HMAC(hashes.SHA256, 32, salt, iterations=320000)
    key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
    f = Fernet(key)
    emsg = f.encrypt(msg.encode())
    return emsg

def decrypt_using_password(pw, emsg):
    try:
        salt = int.to_bytes(int(os.getenv('salt16')), 16, 'little')
    except TypeError as e:
        return "pass the salt"
    kdf = PBKDF2HMAC(hashes.SHA256, 32, salt, iterations=320000)
    key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
    
    cipher = Fernet(key)
    msg = cipher.decrypt(emsg).decode()
    return msg
