import socket
import struct
import time
HOST = '127.0.0.1'
PORT = 6190
addr = (HOST, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.listen()
print('Server is listening')
while True:
    conn, addr = server.accept()
    print('Connected by', addr)
    sizeof_bytes = conn.recv(4)
    sizeof = struct.unpack('!I', sizeof_bytes)[0]

    print(sizeof)
    print(sizeof, "bytes received")
    filename = conn.recv(1024).decode('utf-8')
    print(filename, ' received')
    data = b""
    while len(data) < sizeof:
        packet = conn.recv(sizeof - len(data))
        if not packet:
            break
        data += packet

    with open('b'+filename, 'bx') as f:
        f.write(data)
    conn.close()

