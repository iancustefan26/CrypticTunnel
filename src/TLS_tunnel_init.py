import os
import socket
import rsalib
import random
import string
from file_transfer import send_file
from file_transfer import recive_file

def client_hello(server_sock, name):
    hello = f"Hello, my name is {name}"
    server_sock.sendall(hello.encode('utf-8'))

def server_hello(client_sock, public_key):
    hello_from_client = client_sock.recv(1024).decode('utf-8')
    client_sock.sendall(public_key.encode('utf-8'))

def client_key_exchange(server_sock):
    public_key = server_sock.recv(1024).decode('utf-8')
    session_key = ''.join(random.choice(string.printable) for x in range(30))
    encrypted_random_file = rsalib.rsa_encrypt(session_key, public_key)
    send_file(encrypted_random_file, server_sock)

    return session_key

def recive_key_exchange(client_sock, private_key):
    recive_file("temp.bin", client_sock)
    session_key = rsalib.rsa_decrypt(private_key)
    return session_key



    
    



