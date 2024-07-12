import os
from usable import print_progress
from usable import size_of_file
import aeslib

def send_file(file_path, client_sock, session_key = "", session_iv = ""):
    size, unit = size_of_file(file_path)
    progress_size = 0
    skip_loop = 0
    with open(file_path, "rb") as file:
        chunk = file.read(1024)
        while chunk:
            print(len(chunk))
            if session_key != "":
                if len(chunk) < 1024:
                     chunk = chunk + bytes(1024 - len(chunk))
                encrypted_chunk = aeslib.aes_encrypt(chunk.hex(), session_key.encode().hex(), session_iv).encode()
                chunk = encrypted_chunk
                print(encrypted_chunk)
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
    end_marker = b"END_OF_FILE_TRANSFER"
    if session_key != "":
         before_end_buf = bytes(1024)
         encrypted_buf = aeslib.aes_encrypt(before_end_buf.hex(), session_key.encode().hex(), session_iv).encode()
         client_sock.sendall(encrypted_buf)      
         client_sock.sendall(aeslib.aes_encrypt(end_marker.hex(), session_key.encode().hex(), session_iv).encode())
    else:
        client_sock.sendall(end_marker)
    print_progress(size, size, unit)
    print(f"\n[+] File : {os.path.basename(file_path)} sent succesfully")


def recive_file(file_name, client_sock, session_key = "", session_iv = ""):
    if not os.path.exists(os.getcwd() + "/transfered"):
        os.makedirs(os.getcwd() + "/transfered")
    end_marker = b"END_OF_FILE_TRANSFER"
    buffer = b""
    #print(f"HEY session kei : {session_key}")
    try:
        with open(os.getcwd() + "/transfered/" + file_name, "wb") as file:
                while True:
                    chunk = client_sock.recv(4128)
                    if not chunk:
                        break
                    if session_key != "":
                         print(chunk)
                         decrypted_chunk = bytes.fromhex(bytes.fromhex(aeslib.aes_decrypt(chunk.decode(), session_key.encode().hex(), session_iv)).decode('ascii')).decode('ascii').encode()
                         print(decrypted_chunk)
                         chunk = decrypted_chunk
                    buffer += chunk
                    if end_marker in buffer:
                        file.write(buffer.split(end_marker)[0])
                        break
                    file.write(buffer)
                    buffer = b""
                print(f"[+] File {file_name} recived succesfully.\n")
    except Exception as e:
                print(f"[!] An error has occured when transfering file... : {e}")

