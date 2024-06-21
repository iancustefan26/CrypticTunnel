import socket
import threading
from usable import clear_screen
import curses
import keyboard
from usable import listen_for_key
from file_transfer import recive_file
from usable import get_local_ip

def listen_client(client_sock, client_addr, name):
    clear_screen()
    print(f"Accepted request from Client with IP : {client_addr}")
    client_name = client_sock.recv(100).decode('utf-8')
    print(f"{client_name} has joined.")
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                print("Client has disconnected")
                break
            message = data.decode('utf-8')
            if message[:4] == "SEND":
                file_name = message[5 : len(message)]
                print(f"Reciveing file... : {file_name}")
                recive_file(file_name, client_sock)
            else:
                print(message)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_sock.close()
             
    

def start_server(name):
    host = get_local_ip()
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"Server running on IP: {host} -- PORT: {port} is listening for requests...")
    while True:
        client_sock, client_addr = server_socket.accept()
        listen_client(client_sock, client_addr, name)   
        


if __name__ == "__main__":
    name = input("Type your nickname: ")
    start_server(name)