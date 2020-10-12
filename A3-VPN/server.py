import socket
import sys

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print("Server received: " + data.decode("utf-8"))
            input_var = input("Reply: ")
            input_var = input_var.encode("utf-8")
            conn.sendall(input_var)
