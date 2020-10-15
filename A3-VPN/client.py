import socket
import sys
from queue import Queue
from listen import Listen
from send import Send
from recieve import Receive

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
        self.send_queue = Queue()
        self.receive_queue = Queue()
        self.sendThread = None
        self.receiveThread = None
       
    def connect(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip_addr, self.port))
            self.startSendRecieveThreads()
          
    def send(self, msg):
        self.send_queue.put(msg)

    def receive(self):
        if not self.receive_queue.empty():
            msg = self.receive_queue.get()
            return msg
        else:
            return None

    def startSendRecieveThreads(self):
        self.sendThread = Send(self.socket, self.send_queue, self)
        self.receiveThread = Receive(self.socket, self.receive_queue, self)
        self.sendThread.start()
        self.receiveThread.start()

    def close(self):  
        pass #TODO - do cleanup here