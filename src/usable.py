import socket
import os
from pynput import keyboard

def is_server_running(ip, port, timeout = 5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            #sock.timeout(timeout)
            sock.connect((ip, port))

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

