import socket
import sys

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    while True:
        data = s.recv(1024)
        print('Client Received: ' + data.decode("utf-8"))
        input_var = input("Reply: ")
        input_var = input_var.encode("utf-8")
        s.sendall(input_var)
