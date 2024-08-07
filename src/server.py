import socket
from usable import clear_screen
from file_transfer import recive_file
from usable import get_local_ip
from usable import print_server_info
from TLS_tunnel_init import *
import rsalib
import os

session_iv = ""
session_key = ""

def init_TLS_tunnel(client_sock):
    global session_key, session_iv
    public_key, private_key = rsalib.generateRSAKeyPair()
    server_hello(client_sock, public_key)
    session_key = recive_key_exchange(client_sock, private_key)
    session_iv = client_sock.recv(32).decode()
    print(f"Session key is : {session_key}\nSession iv is : {session_iv}")
    os.remove("transfered/temp.bin")


def listen_client(client_sock, client_addr, name, client_ip):
    clear_screen()
    print(f"[+] Accepted request from Client with IP : {client_addr}")
    client_name = client_sock.recv(100).decode('utf-8')
    print(f"[+] {client_name} has joined.")
    init_TLS_tunnel(client_sock)
    print_server_info(client_addr, 8001, client_name, client_ip)
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                print("[-] Client has disconnected")
                break
            message = data.decode('utf-8')
            if message[:4] == "SEND":
                file_name = message[5 : len(message)]
                size = client_sock.recv(1024).decode('utf-8')
                print(f"[=] {client_name} : wants to send you a file : {file_name}\n[=] Size of file is: {size}")
                response = input("[?] Recive it? (y/n) : ")
                client_sock.sendall(response.encode('utf-8'))
                if response == "y":
                    print(f"[+] Reciveing file... : {file_name}")
                    recive_file(file_name, client_sock, session_key, session_iv)
                else:
                    print("[-] File transfer declined.\n")
                    continue
            elif message[:5] != "/send":
                print(message)
    except Exception as e:
        print(f"[!] An error occurred: {e}")
    finally:
        client_sock.close()
             
    

def start_server(name):
    host = get_local_ip()
    port = 8001
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"[+] Server running on IP: {host} -- PORT: {port} is listening for requests.")
    while True:
        client_sock, client_addr = server_socket.accept()
        listen_client(client_sock, client_addr, name, client_addr)   
        


if __name__ == "__main__":
    name = input("[?] Type your nickname: ")
    start_server(name)