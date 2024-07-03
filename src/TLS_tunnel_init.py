import os
import socket
import rsalib
import random
import string

def client_hello(client_sock, name):
    hello = f"Hello, my name is {name}"
    client_sock.sendall(hello.encode('utf-8'))

def server_hello(server_sock):
    hello_from_client = server_sock.recv(1024).decode('utf-8')
    public_key, private_key = rsalib.generateRSAKeyPair()
    server_sock.sendall(public_key.encode('utf-8'))

def client_key_exchange():
    #public_key = clinet_sock.recv(1024)
    public_key, private_key = rsalib.generateRSAKeyPair()
    random_stuff = ''.join(random.choice(string.printable) for x in range(30))
    print(random_stuff)
    encrypted_stuff_file = rsalib.rsa_encrypt(random_stuff, public_key)
    with open(encrypted_stuff_file, "rb") as f:
        content = f.read(1024)
    print(content)
    decrypted_random = rsalib.rsa_decrypt(private_key)
    print(decrypted_random)

client_key_exchange()
