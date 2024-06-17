import socket
import threading

def listen_client(client_sock, client_addr, name):
    print(f"Accepted request from Client with IP : {client_addr}")
    try:
        client_name = client_sock.recv(1024).decode('utf-8')
        print(f"{client_name} has joined the chat.")
        #client_sock.sendall(name.encode('utf-8'))
    except ConnectionResetError:
            print(f"Connection from {client_addr} has been reset.")
    
    while True:
        #your_message = input(f"{name}: ")

        try:
            # Receive data from the client
            data = client_sock.recv(1024)
            if not data:
                continue
            message = data.decode('utf-8')
            if(message == "disconnected"):
                print(f"{client_name} has left the chat.")
                continue
            print(f"{message}")
        except ConnectionResetError:
            print(f"{client_name} has left the chat.")
            break

    client_sock.close()
             
    

def start_server(name):
    host = "0.0.0.0"
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"Server running on IP: {host} -- PORT: {port} is listening for requests...")

    while True:
        client_sock, client_addr = server_socket.accept()
        threading.Thread(target=listen_client, args=(client_sock, client_addr, name)).start()


if __name__ == "__main__":
    name = input("Type your nickname: ")
    start_server(name)