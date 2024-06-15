import socket
import threading

def listen_client(client_sock, client_addr):
    print(f"Accepted request from Client with IP : {client_addr}")
    

def start_server():
    host = "0.0.0.0"
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"Server running on IP: {host} -- PORT: {port} is listening for requests...")

    while True:
        client_sock, client_addr = server_socket.accept()
        threading.Thread(target=listen_client, args=(client_sock, client_addr)).start()


if __name__ == "__main__":
    start_server()