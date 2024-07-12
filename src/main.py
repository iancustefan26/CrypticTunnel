#!/usr/bin/env python3

import time
import subprocess
from usable import clear_screen

def main():
    clear_screen()
    print("Hello, welcome to CrypticTunnel\nPlease tell us if you want to establish a server or connect to a server")
    response = input("[?] Establish (e) ---- Connect(c) (e/c): ")
    if(response == 'e'):
        print("[...] Establishing server.")
        time.sleep(1)
        #Run server.py
        procces_result = subprocess.run(["python3", "server.py"])
    elif response== 'c':
        print("[...] Setting up client.")
        time.sleep(1)
        #Run client.py
        procces_result = subprocess.run(["python3", "client.py"])
    else:
        print("[!] Invalid option")
        time.sleep(1)
        main()
    if procces_result.returncode == 0:
        print("[+] Script executed succesfully!")
        print("[=] Output: ", procces_result.stdout);
    else:
        print("[!] Script execution failed!")
        print("[!] Error:", procces_result.stderr)


if __name__ == "__main__":
    main()
