import os

def send_file(file_path, client_sock):
    with open(file_path, "rb") as file:
        chunk = file.read(1024)
        while chunk:
            client_sock.sendall(chunk)
            chunk = file.read(1024)
    print(f"File with path: {file_path} sent succesfully")


def recive_file(file_name, client_sock):
    if not os.path.exists(os.getcwd() + "/transfered"):
        os.makedirs(os.getcwd() + "/transfered")
    try:
        with open(os.getcwd() + "/transfered/" + file_name, "wb") as file:
                while True:
                    chunk = client_sock.recv(1024)
                    if not chunk:
                        print("Not chunk")
                        break
                    file.write(chunk)
                print(f"File {file_name} recived succesfully.")
    except Exception as e:
                print(f"An error has occured when transfering file... : {e}")

