import socket
import sys
from queue import Queue
from listen import Listen
from send import Send
from recieve import Receive

class Server:

    def __init__(self, port, shared_key):
        self.port = port
        self.shared_key = shared_key
        self.send_queue = Queue()
        self.receive_queue = Queue()
        self.sendThread = None
        self.receiveThread = None
        self.addr = None
        self.client_socket = None
        self.ip_address = '192.168.1.77' #to be replaced

    def setup(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip_address, self.port))
            self.socket.listen(1)

    def send(self, msg):
        self.send_queue.put(msg)

    def receive(self):
        if not self.receive_queue.empty():
            msg = self.receive_queue.get()
            return msg
        else:
            return None

    def start(self):
        self.listener = Listen(self.socket, self.shared_key, self)
        self.listener.start()

    def startSendRecieveThreads(self, client_socket):
        self.sendThread = Send(client_socket, self.send_queue)
        self.receiveThread = Receive(client_socket, self.receive_queue)
        self.sendThread.start()
        self.receiveThread.start()

    def close(self):
        pass #TODO - do cleanup her
