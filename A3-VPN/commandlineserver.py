import socket
import sys
import random
import os
from Crypto.Cipher import AES
from server import Server

HOST = '192.168.1.77'
PORT = 65432

K_AB = b'123' #input("Hi TA, please enter the shared secret value: ")
K_AB = K_AB.zfill(16) #pad the key to be 16 bytes

server = Server(PORT, K_AB)
server.setup()
server.start()
