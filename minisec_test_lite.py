import serial
import sys
import random
from random import randint
import os
import hashlib
from Crypto.Cipher import AES
import pyDH

outgoingSerial = serial.Serial('COM4',9600,timeout = None)

auth = False
d1prime = 2147483647
d1generator = 16807
b = randint(1000, 9999)
B = (d1generator**b)%(d1prime)

outgoingSerial.write(bytes(str("start"), "utf-8"))
A = outgoingSerial.read() #needs to know length of A incoming

outgoingSerial.write(bytes(str(B), "utf-8")) #not being read on the arduino/esp32 side

while True:
    print('Message: ')
    message = input()
    outgoingSerial.write(bytes(str(message), "utf-8"))
