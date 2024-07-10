import random
import os
import string
import aeslib



plaintext = "Salut, sunt Stefan!"
key = ''.join(random.choice(string.printable) for x in range (30)).encode().hex()
iv = ''.join(random.randbytes(16).hex())

cipher = aeslib.aes_encrypt(plaintext, key, iv)

decrypted = bytes.fromhex(aeslib.aes_decrypt(cipher, key, iv)).decode('ascii')

print(cipher)
print(decrypted)