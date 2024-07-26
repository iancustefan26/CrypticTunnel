# CrypticTunnel - Cryptographic Secured Transfer Tunnel
   ![](https://i.imgur.com/pbQ7EZ9.png)



   

A terminal-based application where two people can securely connect exchanghe files with each other.
The communication will be secured using a TLS tunnel implemented with C++ for the cryptographic operations and Python for managing the connections and user interface.

> *Designed for Unix-based systems*


# Concepts and motivation


 - ****Enhanced Security****
- -   **End-to-End Encryption:** TLS tunnel initialized using RSA encryption, generating a secret session key, and this session key is used for transfer data chunks encrypted with AES256 (for speed I am using symmetrical encryption because asymmetrical algorithms like RSA are slower)
- ![](https://i.imgur.com/P9Ye7At.png)
- -   _Cryptography in C++ for Speed:_ This efficiency is critical when handling large files and real-time chat
-  **Practical Use Cases and user convenience**

- -  **Secure Communication:** Ideal for corporate environments where secure communication is paramount, such as in financial institutions, legal firms, and tech companies handling proprietary information.
- -   **CLI-Based Interface**: A CLI app is lightweight, accessible for advanced users and system administrators who prefer command-line tools

-  **Community and Open Source Contribution**

- -  **Open Source Potential:** By releasing the project as open-source, you can contribute to the community, allowing other developers to use, modify, and improve the application.

![](https://i.imgur.com/kzrY0ms.png)
![](https://i.imgur.com/o8aYIeN.png)


## Useful guide
 - `just type a message once connection is established`
 - 
 - ![enter link description here](https://i.imgur.com/4sinzSN.png)
 - [](https://i.imgur.com/4sinzSN.png)
 - `/send PATH_TO_FILE`
 - - sends a POST request to the server and waiting for response
 - ![](https://i.imgur.com/W7lBTTL.png)
 - ![](https://i.imgur.com/wFaCsgh.png)
 - `/quit`
 - - To exit the client shell
 - ![](https://i.imgur.com/i7EC8tJ.png)





# Technologies Used

 - Python
 - C++
 - OpenSSL
 - Cryptography
 - Networking
 - HTTP and HTTPS protocols concepts
 - Binary exploitation


## Install guide

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/iancustefan26/CrypticTunnel.git
   ```

2. Give permissions to the install script:
	 ```bash
   cd CrypticTunnel
   chmod u+x install.sh
   ```

3. Run the install script:
   ```bash
   ./install.sh
   ```
4. To run the program use the command:
   ```bash
   cytun
   ```

   

## Connect with Me

[LinkedIn](https://www.linkedin.com/in/stefan-teodor-iancu-152a6a284/)

[GitHub](https://www.linkedin.com/in/stefan-teodor-iancu-152a6a284/](https://github.com/iancustefan26))

[Instagram](https://www.instagram.com/iancustefan26/)

Feel free to reach out if you have any questions, feedback, or just want to chat.
