import base64

from Crypto.Cipher import AES


def add_to_16(value:str):
    while len(value) % 16 != 0:
        value += '\0'
    return value.encode('utf-8')

def encrypt(message:str, key:str):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    en_value = aes.encrypt(add_to_16(message))
    return base64.b64encode(en_value).decode("utf-8")

def decrypt(message:str, key:str):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    en_value = aes.decrypt(base64.b64decode(message))
    return en_value.decode("utf-8").replace("\0","")