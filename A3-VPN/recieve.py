import socket
import threading
import sys
import random
import os
from Crypto.Cipher import AES
# Thread used by both client and server.
# Keeps reading messages from the socket and puts the messgae in the queue
class Receive(threading.Thread):

    def __init__(self, socket, queue, shared_key):
        threading.Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.keep_alive = True
        self.shared_key = shared_key

    def run(self):
        # self.socket.setblocking(0)
        while (self.keep_alive):
                try:

                    R = self.socket.recv(16) # receive R_B
                    print("Received a nonce (R): ", R)

                    message = self.socket.recv(1024) # receive E("Bob",R_A,K_AB)
                    print("Client received a message: ", message)

                    aes = AES.new(self.shared_key, AES.MODE_CBC, R)
                    msg = aes.decrypt(message) #decrypt using K_AB and R_A
                    print("Message decrypted to: ", msg)

                    if len(msg) > 0:
                        self.queue.put(msg.decode("utf-8"))

                except socket.error:
                    pass
        self.socket.close()

    def close(self):
        self.keep_alive = False
