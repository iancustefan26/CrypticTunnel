import random
import os
import string
import aeslib


with open("transfered/vuln.c", "rb") as f:
    chunk = f.read(1024)

print(chunk)

plaintext = chunk.hex()
key = ''.join(random.choice(string.printable) for x in range (30)).encode().hex()
iv = ''.join(random.randbytes(16).hex())

cipher = aeslib.aes_encrypt(plaintext, key, iv)
print(cipher)

decrypted = bytes.fromhex(aeslib.aes_decrypt(cipher, key, iv)).decode('ascii')

#print(plaintext)

#print(cipher)
print(bytes.fromhex(decrypted).decode('ascii'))