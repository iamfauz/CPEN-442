import socket
import sys
import random
import os
from Crypto.Cipher import AES
import threading
import time
# Thead used by the server to listen for connection requests
class Listen(threading.Thread):

    def __init__(self, socket, shared_key, server, on_connected_callback):
        threading.Thread.__init__(self)
        self.socket = socket
        self.shared_key = shared_key
        self.server = server
        self.on_connected_callback = on_connected_callback
        self.keep_alive = True
        self.connectionAuth = False

    def run(self):
        # self.socket.setblocking(0)
        while (self.keep_alive) and self.connectionAuth == False:
            client_socket, addr = self.socket.accept()

            #1st arrow in Figure 9.12
            print('Connected by', addr) #eq to "I'm Alice"
            R_A = client_socket.recv(16) #receive R_A
            print("Server received a nonce (R_A): ", R_A)
            R_B = os.urandom(16) # generate R_B

            #2nd arrow in Figure 9.12
            print("Server generated a nonce (R_B): ", R_B)
            client_socket.sendall(R_B) #send R_B
            print("Server sent nonce R_B.")
            message = socket.gethostbyname(socket.gethostname())
            n = len(message)

            if n % 16 != 0:
                message += ' ' * (16 - n % 16) #padded with spaces
                print("Generated plaintext message: ", message)
            aes = AES.new(self.server.shared_key, AES.MODE_CBC, R_A)
            encd = aes.encrypt(message.encode("utf8")) #encrypt "Bob" using R_A and self.server.shared_key
            client_socket.sendall(encd) # send E("Bob",R_A,self.server.shared_key)
            print("Server sent encypted message.")

            #3rd arrow in Figure 9.12
            message = client_socket.recv(1024)
            aes = AES.new(self.server.shared_key, AES.MODE_CBC, R_B)
            decd = aes.decrypt(message) #decrypt using self.server.shared_key and R_A
            client_IP = str(decd.rstrip().decode())
            
            if(client_IP == addr[0]):
                print("Client IP address is a match.")
                print("Authentication is: VALID")
                print('SERVERFOUNDSDIS')
                print(client_socket)
                self.server.client_socket = client_socket

            else:
                print("Client IP address is NOT a match")
                raise Exception("Authentication is: INVALID")

            print('SERVERFOUNDSDIS')
            print(client_socket)
            self.server.client_socket = client_socket
            self.connectionAuth = True
            self.server.startSendRecieveThreads()
            self.on_connected_callback(addr[0], addr[1])
            self.server.clear_queues()

        if not self.keep_alive:
            print('close')
            self.socket.close()

    def close(self):
        self.keep_alive = False
