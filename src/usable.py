import socket
import os

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

