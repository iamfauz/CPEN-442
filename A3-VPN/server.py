import socket
import sys
import random
import os
from Crypto.Cipher import AES

HOST = '127.0.0.1'
PORT = 65432

K_AB = '123' #input("Hi TA, please enter the shared secret value: ")
K_AB = K_AB.zfill(16) #pad the key to be 16 bytes


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        #1st arrow in Figure 9.12
        print('Connected by', addr) #eq to "I'm Alice"
        R_A = conn.recv(16) #receive R_A
        print("Server received a nonce (R_A): ", R_A)
        R_B = os.urandom(16) # generate R_B
        
        #2nd arrow in Figure 9.12
        print("Server generated a nonce (R_B): ", R_B)
        conn.sendall(R_B) #send R_B
        print("Server sent nonce R_B.")
        message = HOST #eq to "Bob"
        n = len(message)
        if n % 16 != 0:
            message += ' ' * (16 - n % 16) #padded with spaces 
        print("Generated plaintext message: ", message)
        aes = AES.new(K_AB, AES.MODE_CBC, R_A)
        encd = aes.encrypt(message) #encrypt "Bob" using R_A and K_AB
        conn.sendall(encd) # send E("Bob",R_A,K_AB)
        print("Server sent encypted message.")

        #3rd arrow in Figure 9.12
        message = conn.recv(1024)
        aes = AES.new(K_AB, AES.MODE_CBC, R_B) 
        decd = aes.decrypt(message) #decrypt using K_AB and R_A
        client_IP = str(decd.rstrip().decode())
        #this authentication will not work atm because program is being run on same machine
        if(client_IP == addr):
            print("Client IP address is a match.")
            print("Authentication is: VALID")
        else: 
            print("Client IP address is NOT a match")
            raise Exception("Authentication is: INVALID")

        #TASK: setup AES encryption for continual communication
        while True:
            data = conn.recv(1024)
            print('Server Received: ' + data.decode("utf-8"))
            input_var = input("Reply: ")
            input_var = input_var.encode("utf-8")
            conn.sendall(input_var)
