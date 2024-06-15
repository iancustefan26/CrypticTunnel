import os
import time

def clear_screen():
    os.system('clear')

def main():
    clear_screen()
    print("Hello, welcome to CrypticTunnel\nPlease tell us if you want to establish a server or connect to a server")
    response = input("Establish (e) ---- Connect(c) (e/c): ")
    if(response == 'e'):
        print("Establishing server...")
        time.sleep(1)
        #Run server.py
    elif response== 'c':
        print("Setting up client...")
        time.sleep(1)
        #Run client.py
    else:
        print("Invalid option")
        time.sleep(1)
        main()


if __name__ == "__main__":
    main()
