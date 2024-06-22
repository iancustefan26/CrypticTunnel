import os
from usable import print_progress


def size_of_file(file_path):
    file_size = os.stat(file_path).st_size / (1024 * 1024)
    if file_size > 1000:
         return round(file_size / 1024, 2), "GB"
    return round(file_size, 2), "MB"

def send_file(file_path, client_sock):
    size, unit = size_of_file(file_path)
    #send size, unit #
    #client_sock.sendall((len(str(size) + 2), str(size), unit))
    progress_size = 0
    skip_loop = 0
    with open(file_path, "rb") as file:
        chunk = file.read(1024)
        while chunk:
            client_sock.sendall(chunk)
            skip_loop += 1
            if unit == "MB":
                progress_size += 1 / 1024
            else: 
                progress_size += 1 / (1024 * 1024)
            if skip_loop > 1500:
                 print_progress(progress_size, size, unit)
                 skip_loop = 0
            chunk = file.read(1024)
    end_marker = "END_OF_FILE_TRANSFER"
    client_sock.sendall(end_marker.encode('utf-8'))
    print_progress(progress_size, size, unit)
    print(f"\nFile : {os.path.basename(file_path)} sent succesfully")


def recive_file(file_name, client_sock):
    if not os.path.exists(os.getcwd() + "/transfered"):
        os.makedirs(os.getcwd() + "/transfered")
    end_marker = b"END_OF_FILE_TRANSFER"
    buffer = b""
    #length = client_sock.recv(4)
   # size, unit = client_sock.recv(length)
    #print(size, unit)

    try:
        with open(os.getcwd() + "/transfered/" + file_name, "wb") as file:
                while True:
                    chunk = client_sock.recv(1024)
                    if not chunk:
                        break
                    buffer += chunk
                    if end_marker in buffer:
                        file.write(buffer.split(end_marker)[0])
                        break
                    file.write(buffer)
                    buffer = b""
                print(f"File {file_name} recived succesfully.\n")
    except Exception as e:
                print(f"An error has occured when transfering file... : {e}")

