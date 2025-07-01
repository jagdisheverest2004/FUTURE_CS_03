from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

KEY = b'ThisIsASecretKey'  # 16 bytes key for AES-128

def pad(data):
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_file(data):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data))
    return iv + encrypted_data  # Prepend IV

def decrypt_file(encrypted_data):
    iv = encrypted_data[:16]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    original_data = unpad(cipher.decrypt(encrypted_data[16:]))
    return original_data
