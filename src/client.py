import socket
import threading
from usable import clear_screen
from usable import is_server_running
import time


def connect_to_server(server_addr, server_port, name):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((server_addr, server_port))
    print(f"Connect to the server -- IP : {server_addr} -- PORT : {server_port}")
    print("Starting chat session...")
    try:
        client_sock.sendall(name.encode('utf-8'))
        #server_name = client_sock.recv(1024).decode('utf-8')
        #print(f"You ar talking to {server_name}")
    except:
        print("Error")
    time.sleep(2)
    clear_screen()
    while True:
        client_message = name + ": " + input(f"{name}: ")
        if client_message[len(name) + 2:] == "/quit":
            client_sock.sendall("disconnected".encode('utf-8'))
            break
        try:
            client_sock.sendall(client_message.encode('utf-8'))
        except:
            print("Host has disconnected; try /quit")
    client_sock.close()
    print("Disconnected from the server")


def main():
    clear_screen()
    name = input("Type your nickname: ")
    server_addres = input("Please type the server's IP addres: ")
    server_port = input("Please type the server's PORT: ")
    server_port = int(server_port)
    if not is_server_running(server_addres, server_port):
        print("the server you are attempting to connect is not running or can't connect!; Please try again")
        time.sleep(2)
        main()
    else:
        print(f"Attempting to connect to server IP : {server_addres} with PORT : {server_port}")
        connect_to_server(server_addres, server_port, name)

if __name__ == "__main__":
    main()

