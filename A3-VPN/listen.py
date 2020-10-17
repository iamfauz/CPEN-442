import socket
import sys
import random
import os
from Crypto.Cipher import AES
import threading
import time
import hashlib
# Thead used by the server to listen for connection requests
class Listen(threading.Thread):

    def __init__(self, socket, shared_key, server, on_connected_callback, app):
        threading.Thread.__init__(self)
        self.socket = socket
        self.shared_key = shared_key
        self.server = server
        self.on_connected_callback = on_connected_callback
        self.keep_alive = True
        self.connectionAuth = False
        self.connectionSteps = 5
        self.app = app

    def run(self):
        # self.socket.setblocking(0)

        while (self.keep_alive) and self.connectionAuth == False:
            self.app.connection_steps = 1

            print(self.app.connection_steps)
            client_socket, addr = self.socket.accept()

            #1st arrow in Figure 9.12
            print('Connected by', addr) #eq to "I'm Alice"
            R_A = client_socket.recv(16) #receive R_A

            print("Server received a nonce (R_A): ", R_A)

            if self.app.debug_mode == True:
                debug_s1 = "Server received a nonce (R_A): " + str(R_A)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            R_B = os.urandom(16) # generate R_B

            while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 1:
                time.sleep(0.1)

            #generation of key K_AB
            keyHash = hashlib.md5(self.server.shared_key + R_A)
            self.shared_key = keyHash.digest()
            self.server.shared_key = self.shared_key
            print('The fresh session key is ', self.shared_key)

            if self.app.debug_mode == True:
                debug_s1 = "Fresh session key: " + str(self.shared_key)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 2:
                time.sleep(0.1)

            #2nd arrow in Figure 9.12
            print("Server generated a nonce (R_B): ", R_B)
            client_socket.sendall(R_B) #send R_B
            print("Server sent nonce R_B.")
            
            if self.app.debug_mode == True:
                debug_s1 = "Server sent a nonce (R_B): " + str(R_B)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            message = socket.gethostbyname(socket.gethostname())
            n = len(message)
            if n % 16 != 0:
                message += ' ' * (16 - n % 16) #padded with spaces
            print("Generated plaintext message: ", message)

            if self.app.debug_mode == True:
                debug_s1 = "Server sent nonce (R_B): " + str(R_B)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 3:
                time.sleep(0.1)

            aes = AES.new(self.server.shared_key, AES.MODE_CBC, R_A)
            encd = aes.encrypt(message.encode("utf8")) #encrypt "Bob" using R_A and self.server.shared_key
            client_socket.sendall(encd) # send E("Bob",R_A,self.server.shared_key)
            print("Server sent encypted message: ", encd)

            if self.app.debug_mode == True:
                debug_s1 = "Server encrypted message using AES: " + str(encd)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 4:
                time.sleep(0.1)

            #3rd arrow in Figure 9.12
            message = client_socket.recv(1024)
            aes = AES.new(self.server.shared_key, AES.MODE_CBC, R_B)
            decd = aes.decrypt(message) #decrypt using self.server.shared_key and R_A
            client_IP = str(decd.rstrip().decode())
            if self.app.debug_mode == True:
                debug_s1 = "Client_IP after decryption: " + str(client_IP)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 0:
                time.sleep(0.1)

            if(client_IP == addr[0]):
                print("Client IP address is a match.")
                print("Authentication is: VALID")
                self.server.client_socket = client_socket

            else:
                print("Client IP address is NOT a match")
                raise Exception("Authentication is: INVALID")

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
