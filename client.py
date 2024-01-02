import socket
import struct

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
client.send(filename.encode('utf-8'))
client.sendall(_bytes)
client.close()
