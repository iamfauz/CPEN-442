import socket
import sys
from queue import Queue
from listen import Listen
from send import Send
from recieve import Receive

class Server:

    def __init__(self, port, shared_key, on_connected_callback, debug_mode, app):
        self.port = port
        self.shared_key = shared_key
        self.on_connected_callback = on_connected_callback
        self.send_queue = Queue()
        self.receive_queue = Queue()
        self.sendThread = None
        self.receiveThread = None
        self.connectionAuth = False
        self.client_socket = None
        self.debugMode = debug_mode
        self.app = app

    def setup(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('', self.port))
            self.socket.listen(1)
            return ("Server listening on port " + str(self.port))

    def send(self, msg):
        self.send_queue.put(msg)

    def receive(self):
        if not self.receive_queue.empty():
            msg = self.receive_queue.get()
            return msg
        else:
            return None

    def start(self):
        self.listener = Listen(self.socket, self.shared_key, self, self.on_connected_callback, self.app)
        self.listener.start()

    def startSendRecieveThreads(self):
        print('Start server send receive threads...')
        print(self.client_socket)
        self.sendThread = Send(self.client_socket, self.send_queue, self.shared_key, self.debugMode, self.app)
        self.receiveThread = Receive(self.client_socket, self.receive_queue, self.shared_key, self.debugMode, self.app)
        self.sendThread.start()
        self.receiveThread.start()

    def clear_queues(self):
        self.receive_queue.queue.clear()
        self.send_queue.queue.clear()
    def close(self):
        pass #TODO - do cleanup her
