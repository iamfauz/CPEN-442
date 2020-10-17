import socket
import threading
import sys
import random
import os
from Crypto.Cipher import AES
# Thread used by both client and server.
# Keeps reading messages from the socket and puts the messgae in the queue
class Receive(threading.Thread):

    def __init__(self, socket, queue, shared_key, debug_mode, app):
        threading.Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.keep_alive = True
        self.shared_key = shared_key
        self.connectionSteps = 3
        self.app = app
        self.app.connection_steps = 1

    def run(self):
        # self.socket.setblocking(0)
        while (self.keep_alive):
                try:

                    R = self.socket.recv(16) # receive R_B
                    print("Received a nonce (R): ", R)

                    if self.app.debug_mode == True:
                        debug_s1 = "Received nonce R: " + str(R)
                        self.app.chat_window.write_message("DEBUG", debug_s1)

                    while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 1:
                        pass

                    message = self.socket.recv(1024) # receive E("Bob",R_A,K_AB)
                    print("Received a message: ", message)

                    if self.app.debug_mode == True:
                        debug_s1 = "Received message: " + str(message)
                        self.app.chat_window.write_message("DEBUG", debug_s1)

                    while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 2:
                        pass

                    aes = AES.new(self.shared_key, AES.MODE_CBC, R)
                    msg = aes.decrypt(message) #decrypt using K_AB and R_A
                    print("Message decrypted to: ", msg)

                    if self.app.debug_mode == True:
                        debug_s1 = "Received message decrypted to: " + str(msg)
                        self.app.chat_window.write_message("DEBUG", debug_s1)

                    if len(msg) > 0:
                        self.queue.put(msg.decode("utf-8"))

                except socket.error:
                    pass
        self.socket.close()

    def close(self):
        self.keep_alive = False
