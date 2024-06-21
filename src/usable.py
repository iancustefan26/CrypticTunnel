import socket
import os
from pynput import keyboard
import requests

def is_server_running(ip, port, timeout = 5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
            #sock.timeout(timeout)
            print(f"Trying to connect to {ip}")
            try:
                client_sock.connect((ip, port))
                print(f"Connected to server {ip}:{port}")
            except ConnectionRefusedError:
                print(f"Connection to {ip}:{port} refused")
            except socket.timeout:
                print("Connection timed out")
            except Exception as e:
                print(f"Error connecting to server: {e}")
            finally:
                client_sock.close()
            print("Connected")
            return True
    except (socket.timeout, socket.error):
        return False


def clear_screen():
    os.system('clear')


def on_press(key):
    try:
        # Check if the 'i' key is pressed
        if key.char == 'i':
            print('You pressed "i"!')
            return False  # Stop listener
    except AttributeError:
        # Handle special keys that do not have a char attribute
        pass

def listen_for_key():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = "127.0.0.1"  #Fallback
        print(f"Fallback IP adress {local_ip}")
    finally:
        s.close()
    return local_ip

def get_public_ip():
    try:
        response = requests.get('https://ipinfo.io/ip')
        print(response)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"Failed to retrieve IP address. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error: {e}")
    
    return None

