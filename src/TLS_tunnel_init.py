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
    #print("Printed hello from client")

def server_hello(client_sock, public_key):
    #print("Waiting for client hello...")
    hello_from_client = client_sock.recv(1024).decode('utf-8')
    #print(hello_from_client)
    client_sock.sendall(public_key.encode('utf-8'))

def client_key_exchange(server_sock):
    public_key = server_sock.recv(1024).decode('utf-8')
    #print(f"Public key is: {public_key}")
    session_key = ''.join(random.choice(string.printable) for x in range(30))
    #print(f"Before sending: {session_key}")
    encrypted_random_file = rsalib.rsa_encrypt(session_key, public_key)
    #print(f"Session key generated from file is : {session_key}")
    send_file(encrypted_random_file, server_sock)

    return session_key

def recive_key_exchange(client_sock, private_key):
    recive_file("temp.bin", client_sock)
    #print(f"Private key is: {private_key}")
    session_key = rsalib.rsa_decrypt(private_key)
    #print(f"After recive: {session_key}")
    return session_key



    
    



