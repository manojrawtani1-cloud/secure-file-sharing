from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# AES-256 key (32 bytes)
KEY = b'InterneeFileKey1234567890123456!'
IV = b'InterneeFileIV12'

def encrypt_file(file_data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(file_data, AES.block_size))
    return encrypted

def decrypt_file(encrypted_data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted