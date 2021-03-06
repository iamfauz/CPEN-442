import socket
import sys
import random
import os
import hashlib
from Crypto.Cipher import AES
from queue import Queue
from listen import Listen
from send import Send
from recieve import Receive
import time

class Client:

    def __init__(self, ip_addr, port, shared_key, debug_mode, app):
        self.ip_addr = ip_addr
        self.port = port
        self.shared_key = shared_key
        self.send_queue = Queue()
        self.receive_queue = Queue()
        self.sendThread = None
        self.receiveThread = None
        self.connectionAuth = False
        self.connectionSteps = 5
        self.app = app

    def connect(self):
            self.app.connection_steps = 0

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip_addr, self.port))

            #Point 1
            R_A = os.urandom(16) # generate R_A
            print("Client generated a nonce (R_A): ", R_A)
            self.socket.sendall(R_A) #send R_A
            print("Client sent nonce R_A.")

            if self.app.debug_mode == True:
                debug_s1 = "Client sent nonce (R_A): " + str(R_A)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            # while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 1:
            #     pass

            #generation of key K_AB fresh session key
            keyHash = hashlib.md5(self.shared_key + R_A)
            self.shared_key = keyHash.digest()
            print('The fresh session key is ', self.shared_key)

            if self.app.debug_mode == True:
                debug_s1 = "Fresh session key: " + str(self.shared_key)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            # while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 2:
            #     pass

            #Point2: 2nd arrow in Figure 9.12
            R_B = self.socket.recv(16) # receive R_B
            print("Client received a nonce (R_B): ", R_B)
            message = self.socket.recv(1024) # receive E("Bob",R_A,K_AB)
            print("Client received a message: ", message)

            if self.app.debug_mode == True:
                debug_s1 = "Client received a nonce (R_B): " + str(R_B)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            if self.app.debug_mode == True:
                debug_s1 = "Client received a message: " + str(message)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            # while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 3:
            #     pass

            aes = AES.new(self.shared_key, AES.MODE_CBC, R_A)
            decd = aes.decrypt(message) #decrypt using K_AB and R_A
            server_IP = str(decd.rstrip().decode())
            print("Decrypted message to be: ", server_IP)

            if self.app.debug_mode == True:
                debug_s1 = "Decrypted server IP using session key: " + str(server_IP)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            # while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 4:
            #     pass

            if(server_IP == self.ip_addr):
                print("Server IP address is a match.")
                print("Authentication is: VALID")
                if self.app.debug_mode == True:
                    self.app.chat_window.write_message("DEBUG", "Authentication is: VALID")
                self.connectionAuth = True
            else:
                if self.app.debug_mode == True:
                    self.app.chat_window.write_message("DEBUG", "Authentication is: INVALID")
                print("Server IP address is NOT a match")
                raise Exception("Authentication is: INVALID")

            # while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 0:
            #     pass

            #Point 3: 3rd arrow in Figure 9.12
            message = socket.gethostbyname(socket.gethostname()) # get own IP
            n = len(message)
            if n % 16 != 0:
                message += ' ' * (16 - n % 16) #padded with spaces
            aes = AES.new(self.shared_key, AES.MODE_CBC, R_B)
            encd = aes.encrypt(message.encode("utf8")) #encrypt "Alice" using R_B and K_AB
            self.socket.sendall(encd) #send E("Alice",R_B,K_AB)
            print("Client send ecrypted message: ", encd)
            if self.app.debug_mode == True:
                debug_s1 = "Client send ecrypted message: " + str(encd)
                self.app.chat_window.write_message("DEBUG", debug_s1)

            self.startSendRecieveThreads()
            return ("Connected to Server (%s, %i)" % (self.ip_addr, self.port))

    def send(self, msg):
        self.send_queue.put(msg)

    def receive(self):
        if not self.receive_queue.empty():
            msg = self.receive_queue.get()
            return msg
        else:
            return None

    def startSendRecieveThreads(self):
        print("Client starting send receive threads...")
        self.sendThread = Send(self.socket, self.send_queue, self.shared_key, self.app.debug_mode, self.app)
        self.receiveThread = Receive(self.socket, self.receive_queue, self.shared_key, self.app.debug_mode, self.app)
        self.sendThread.start()
        self.receiveThread.start()

    def clear_queues(self):
        self.receive_queue.queue.clear()
        self.send_queue.queue.clear()
    def close(self):
        pass #TODO - do cleanup here
