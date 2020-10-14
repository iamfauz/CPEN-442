import socket
import sys

# HOST = '127.0.0.1'
# PORT = 65432

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     while True:
#         data = s.recv(1024)
#         print('Client Received: ' + data.decode("utf-8"))
#         input_var = input("Reply: ")
#         input_var = input_var.encode("utf-8")
#         s.sendall(input_var)

class Client:
    
    def __init__(self, ip_addr, port, shared_key):
        self.ip_addr = ip_addr
        self.port = port
        self.shared_key = shared_key
       
    def connect(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip_addr, self.port))
          
    def send(self, msg):
        self.socket.sendall(msg)
        while True:
            data = self.socket.recv(1024)
            print('Client Received: ' + data.decode("utf-8"))
            input_var = input("Reply: ")
            input_var = input_var.encode("utf-8")
            self.socket.sendall(input_var)

        