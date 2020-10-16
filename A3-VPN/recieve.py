import socket
import threading

# Thread used by both client and server.
# Keeps reading messages from the socket and puts the messgae in the queue
class Receive(threading.Thread):

    def __init__(self, socket, queue):
        threading.Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.keep_alive = True

    def run(self):
        print('rec')
        print(self.socket)
        self.socket.setblocking(0)
        while (self.keep_alive):
                try:
                    msg = self.socket.recv(8192)
                    if len(msg) == 0:
                        # Server has closed the socket, exit the program
                        print('Lost connection to the server!')
                        self.socket.close()

                    self.queue.put(msg.decode("utf-8"))
                except socket.error:
                    pass
        self.socket.close()

    def close(self):
        self.keep_alive = False
