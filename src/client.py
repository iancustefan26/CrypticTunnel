import socket
import threading
from usable import clear_screen
from usable import is_server_running
import time


def connect_to_server(server_addr, server_port):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((server_addr, server_port))
    print(f"Connect to the server -- IP : {server_addr} -- PORT : {server_port}")
    while True:
        #the send message loop
        break
    client_sock.close()
    print("Disconnected from the server")


def main():
    clear_screen()
    server_addres = input("Please type the server's IP addres: ")
    server_port = input("Please type the server's PORT: ")
    server_port = int(server_port)
    if not is_server_running(server_addres, server_port):
        print("the server you are attempting to connect is not running or can't connect!; Please try again")
        time.sleep(2)
        main()
    else:
        print(f"Attempting to connect to server IP : {server_addres} with PORT : {server_port}")
        connect_to_server(server_addres, server_port)

if __name__ == "__main__":
    main()

