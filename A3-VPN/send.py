  
import socket
import threading

# Thread used by both client and server.
# Keeps reading messages from the queue and sends the message over the connection
class Send(threading.Thread):

    def __init__(self, socket, queue):
        threading.Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.keep_alive = True 
    
    # Keep reading from the queue and send 
    def run(self):
        self.socket.setblocking(0)
        while (self.keep_alive):  
            if not self.queue.empty():
                msg = self.queue.get()
                self.socket.sendall(msg.encode("utf-8"))
        self.socket.close()

    def close(self):
        self.keep_alive = False