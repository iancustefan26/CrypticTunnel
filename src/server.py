import socket
import threading

def start_server():
    host = "0.0.0.0"
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"Server running on IP: {host} -- Port:{port} is listening for requests...")

if __name__ == "__main__":
    start_server()