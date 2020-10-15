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
    #1st arrow in Figure 9.12
    s.connect((HOST, PORT))
    R_A = os.urandom(16) # generate R_A
    print("Client generated a nonce (R_A): ", R_A)
    s.sendall(R_A) #send R_A
    print("Client sent nonce R_A.")
    
    #2nd arrow in Figure 9.12
    R_B = s.recv(16) # receive R_B
    print("Client received a nonce (R_B): ", R_B)
    message = s.recv(1024) # receive E("Bob",R_A,K_AB)
    print("Client received a message: ", message)
    aes = AES.new(K_AB, AES.MODE_CBC, R_A) 
    decd = aes.decrypt(message) #decrypt using K_AB and R_A
    server_IP = str(decd.rstrip().decode())
    if(server_IP == HOST):
        print("Server IP address is a match.")
        print("Authentication is: VALID")
    else: 
        print("Server IP address is NOT a match")
        raise Exception("Authentication is: INVALID")

    #3rd arrow in Figure 9.12
    message = socket.gethostbyname(socket.gethostname()) # get own IP
    n = len(message)
    if n % 16 != 0:
        message += ' ' * (16 - n % 16) #padded with spaces 

    aes = AES.new(K_AB, AES.MODE_CBC, R_B)
    encd = aes.encrypt(message) #encrypt "Alice" using R_B and K_AB
    s.sendall(encd) #send E("Alice",R_B,K_AB)

    #TASK: setup AES encryption for continual communication
    while True:
        data = s.recv(1024)
        print('Client Received: ' + data.decode("utf-8"))
        input_var = input("Reply: ")
        input_var = input_var.encode("utf-8")
        s.sendall(input_var)
