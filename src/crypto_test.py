import rsalib
import time
import os

public_key, private_key = rsalib.generateRSAKeyPair()

plaintext = "Salut, sunt Stefan"

out_file = rsalib.rsa_encrypt(plaintext, public_key)

with open(out_file, "rb") as f:
    data = f.read(1024)

printable_data = ''.join([chr(byte) for byte in data])

print(printable_data)

decrypted_plain = rsalib.rsa_decrypt(private_key)

os.remove(out_file)

print(decrypted_plain)


