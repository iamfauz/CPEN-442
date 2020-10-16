import socket
import threading

# Thead used by the server to listen for connection requests
class Listen(threading.Thread):
    
    def __init__(self, socket, shared_key, server, on_connected_callback):
        threading.Thread.__init__(self)    
        self.socket = socket
        self.shared_key = shared_key
        self.server = server 
        self.on_connected_callback = on_connected_callback
        self.keep_alive = True

    def run(self):
        self.socket.setblocking(0)

        while (self.keep_alive):
            try: 
                client_socket, addr = self.socket.accept()
                self.server.startSendRecieveThreads(client_socket)
                self.on_connected_callback(addr[0], addr[1])
                self.server.clear_queues()
                # Do auth here
            except socket.error:
                pass
        if not self.keep_alive:
            self.socket.close()

    def close(self):
        self.keep_alive = False
    