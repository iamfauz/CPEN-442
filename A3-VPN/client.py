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
    s.connect((HOST, PORT))
    R_A = os.urandom(16) # generate R_A
    print("Client generated a nonce (R_A): ", R_A)
    s.sendall(R_A) #send R_A
    print("Client sent nonce R_A.")
    R_B = s.recv(16) # receive R_B
    print("Client received a nonce (R_B): ", R_B)
    message = s.recv(1024) # receive E("Bob",R_A,K_AB)
    print("Client received a message: ", message)
    #next step: extract IP ("Bob") and R_A from message by decrypting


    while True:
        data = s.recv(1024)
        print('Client Received: ' + data.decode("utf-8"))
        input_var = input("Reply: ")
        input_var = input_var.encode("utf-8")
        s.sendall(input_var)
