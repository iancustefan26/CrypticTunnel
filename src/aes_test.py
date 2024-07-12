import random
import os
import string
import aeslib


with open("/Users/stefaniancu/Downloads/vuln.c", "rb") as f:
    chunk = f.read(1024)

#print(chunk)

plaintext = b'fd4b7fa47769d68cb775ff2710b60730301468c968e4156598a8c1009ff573711c40385973f588ca5607ce99a8827edc'
key = "7Kca,V43he3*X{(_2D<ksBs?D$w'tj"
iv = "04efbb0e44ac92bad9e6008cc6157230"

decrypted = bytes.fromhex(bytes.fromhex(aeslib.aes_decrypt(plaintext.decode(), key.encode().hex(), iv)).decode('ascii')).decode('ascii')

print(decrypted)

#cipher = aeslib.aes_encrypt(plaintext, key, iv).encode()
#print(cipher)

#decrypted = bytes.fromhex(aeslib.aes_decrypt(cipher.decode(), key, iv)).decode('ascii')
#print(decrypted)
#print(plaintext)

#print(cipher)
#print(bytes.fromhex(decrypted).decode('ascii'))