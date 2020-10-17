import sys
import random
import os
from Crypto.Cipher import AES
import socket
import threading

# Thread used by both client and server.
# Keeps reading messages from the queue and sends the message over the connection
class Send(threading.Thread):

    def __init__(self, socket, queue, shared_key, debugMode, app):
        threading.Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.shared_key = shared_key
        self.keep_alive = True
        self.connectionSteps = 3
        self.app = app
        self.app.connection_steps = 1

    # Keep reading from the queue and send
    def run(self):
        while (self.keep_alive):
            if not self.queue.empty():
                try:

                    R = os.urandom(16) # generate R_A
                    print("Generated a nonce (R): ", R)

                    if self.app.debug_mode == True:
                        debug_s1 = "Generated nonce (R): " + str(R)
                        self.app.chat_window.write_message("DEBUG", debug_s1)

                    while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 1:
                        pass

                    self.socket.sendall(R) #send R_A
                    print("Sent nonce R.")
                    if self.app.debug_mode == True:
                        debug_s1 = "Sent nonce R"
                        self.app.chat_window.write_message("DEBUG", debug_s1)

                    while self.app.debug_mode and self.app.connection_steps % self.connectionSteps == 2:
                        pass

                    aes = AES.new(self.shared_key, AES.MODE_CBC, R)
                    msg = self.queue.get()
                    n = len(msg)
                    if n % 16 != 0:
                        msg += ' ' * (16 - n % 16) #padded with spaces

                    encd = aes.encrypt(msg.encode("utf8"))
                    self.socket.sendall(encd)
                    print("Encrypted message sent: ", encd)
                    if self.app.debug_mode == True:
                        debug_s1 = "Sent encrypted message: " + str(encd)
                        self.app.chat_window.write_message("DEBUG", debug_s1)
                        
                except socket.error:
                    pass

        self.socket.close()

    def close(self):
        self.keep_alive = False
