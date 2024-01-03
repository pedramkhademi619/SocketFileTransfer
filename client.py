import socket
import struct
from time import sleep
HOST = '127.0.0.1'
PORT = 6190
addr = (HOST, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)
print("Connected to server")
print("Enter your filename: ", end='')
filename = input()
print(filename)
with open(filename, 'rb') as f:
    _bytes = f.read()
    sizeof = len(_bytes)
client.send(struct.pack("!I", sizeof))
client.send(filename[::-1].encode('utf-8'))
print(client.recv(20).decode('utf-8'))
client.sendall(_bytes)
statusOfFile = client.recv(100).decode('utf-8')
print(statusOfFile)
client.close()
