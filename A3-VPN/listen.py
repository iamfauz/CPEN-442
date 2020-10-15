import socket
import threading

# Thead used by the server to listen for connection requests
class Listen(threading.Thread):
    
    def __init__(self, socket, shared_key, server):
        threading.Thread.__init__(self)    
        self.socket = socket
        self.shared_key = shared_key
        self.server = server 

    def run(self):
        self.socket.setblocking(0)

        while (self.keep_alive):
           
            client_socket, addr = self.socket.accept()
            self.server.startSendRecieveThreads(client_socket)
            # Do auth here
            
        if not self.keep_alive:
            self.socket.close()

    def close(self):
        self.keep_alive = False
    