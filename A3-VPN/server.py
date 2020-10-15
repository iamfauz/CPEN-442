import socket
import sys
import random
import os
from Crypto.Cipher import AES

HOST = '127.0.0.1'
PORT = 65432

K_AB = input("Hi TA, please enter the shared secret value: ")
K_AB = K_AB.zfill(16) #pad the key to be 16 bytes


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr) #eq to "I'm Alice"
        R_A = conn.recv(16) #receive R_A
        print("Server received a nonce (R_A): ", R_A)
        R_B = os.urandom(16) # generate R_B
        print("Server generated a nonce (R_B): ", R_B)
        conn.sendall(R_B) #send R_B
        print("Server sent nonce R_B.")
        message = HOST + str(R_A) #concantenate "Bob" and R_A
        n = len(message)
        if n % 16 != 0:
            message += '0' * (16 - n % 16) #padded with spaces 
        print("Generated plaintext message: ", message)
        print('The length of the message is ', len(message))
        aes = AES.new(K_AB, AES.MODE_CBC, R_B)
        encd = aes.encrypt(message)
        conn.sendall(encd) # send E("Bob",R_A,K_AB)
        print("Server sent encypted message.")

        while True:
            data = conn.recv(1024)
            print('Server Received: ' + data.decode("utf-8"))
            input_var = input("Reply: ")
            input_var = input_var.encode("utf-8")
            conn.sendall(input_var)
