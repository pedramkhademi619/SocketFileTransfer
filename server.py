import socket
import struct
import time
import threading
import filetype

HOST = '127.0.0.1'
PORT = 6190
addr = (HOST, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.listen()
print('Server is listening')


def handle_connection(conn, _addr):
    print('Connected by', _addr)

    sizeof_bytes = conn.recv(4)
    sizeof = struct.unpack('!I', sizeof_bytes)[0]
    print(sizeof)
    print(sizeof, "bytes received")
    try:
        filename = conn.recv(24).decode('utf-8')[::-1]
        conn.send("File name received".encode('utf-8'))

    except UnicodeDecodeError:
        filename = "Unknown!"
        conn.send("File name not received".encode('utf-8'))

    data = b""
    while len(data) < sizeof:
        packet = conn.recv(sizeof - len(data))
        if not packet:
            break
        data += packet
    statusOfFile = ''
    try:
        with open('b' + filename, 'xb') as f:
            f.write(data)
        statusOfFile = 'File successfully write'
    except FileExistsError:
        with open('b' + filename + '(1)', 'xb') as f:
            f.write(data)
        statusOfFile = 'File name exists. File b{}(1) is created'.format(filename)
    finally:
        conn.send(statusOfFile.encode('utf-8'))

        conn.close()


while True:
    connection, address = server.accept()
    thread = threading.Thread(target=handle_connection, args=(connection, address))
    thread.start()
