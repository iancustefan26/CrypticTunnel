import socket
import os
import requests
import sys

def is_server_running(ip, port, timeout = 5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
            #sock.timeout(timeout)
            print(f"[...] Trying to connect to {ip}")
            try:
                client_sock.connect((ip, port))
                print(f"[+] Connected to server {ip}:{port}")
            except ConnectionRefusedError:
                print(f"[!] Connection to {ip}:{port} refused")
            except socket.timeout:
                print("[!] Connection timed out")
            except Exception as e:
                print(f"[!] Error connecting to server: {e}")
            finally:
                client_sock.close()
            #print("Connected")
            return True
    except (socket.timeout, socket.error):
        return False


def clear_screen():
    os.system('clear')


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = "127.0.0.1"  #Fallback
        print(f"[.] Fallback IP adress {local_ip}")
    finally:
        s.close()
    return local_ip

def get_public_ip():
    try:
        response = requests.get('https://ipinfo.io/ip')
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"[!] Failed to retrieve IP address. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"[!] Error: {e}")
    
    return None

def print_progress(current_size, total_size, unit):
    if total_size != 0:
        progress = (current_size / total_size) * 100
    else:
        return
    sys.stdout.write(f"\r{current_size:.2f} {unit} / {total_size:.2f} {unit} ({progress:.2f}%)")
    sys.stdout.flush()


def size_of_file(file_path):
    file_size = os.stat(file_path).st_size / (1024 * 1024)
    if file_size > 1000:
         return round(file_size / 1024, 2), "GB"
    return round(file_size, 2), "MB"


def print_server_info(ip, port, client_name, client_ip):
    print(f"\n\n      Server IP: {ip}     PORT: {port}", end = "\n\n")
    print(f"     Client's IP: {client_ip}   Client's name: {client_name}", end = "\n\n")
    print("--------------------------------------------------")