import socket
import struct
from time import sleep
import threading
import os

HOST = '127.0.0.1'
PORT = 6190
addr = (HOST, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.listen()
print('Server is listening')


def get(_conn):
    sizeof_bytes = _conn.recv(4)
    sizeof = struct.unpack('!I', sizeof_bytes)[0]
    print(sizeof)
    print(sizeof, "bytes received")
    try:
        filename = _conn.recv(24).decode('utf-8')[::-1]
        sleep(1)
        _conn.send("server>>File name received".encode('utf-8'))

    except UnicodeDecodeError:
        filename = "Unknown!"

    data = b""
    while len(data) < sizeof:
        packet = _conn.recv(sizeof - len(data))
        if not packet:
            break
        data += packet
    statusOfFile = ''
    try:
        with open('b' + filename, 'xb') as f:
            f.write(data)
        statusOfFile = 'server>>File successfully write in Server:{}'.format(os.path.abspath('b' + filename))
    except FileExistsError:
        _filename = 'b' + filename
        with open('1' + _filename, 'xb') as f:
            f.write(data)
        statusOfFile = 'server>>File name exists. File 1b{} is saved in Server:{}.'.format(filename, os.path.abspath(
            'b' + filename))
    finally:
        _conn.send(statusOfFile.encode('utf-8'))


def put(_conn):
    filename = _conn.recv(1024).decode('utf-8')[::-1]
    _conn.send("server>>File name received".encode('utf-8'))

    with open(filename, 'rb') as f:
        _bytes = f.read()
        sizeof = len(_bytes)
    _conn.send(struct.pack("!I", sizeof))
    _conn.sendall(_bytes)


def handle_connection(_conn, _addr, _task):
    # Critical Session
    mutex = threading.Lock()
    mutex.acquire()
    print('Connected by', _addr)
    if task == 'put':
        get(_conn)
    elif task == 'get':
        put(_conn)
    _conn.close()
    mutex.release()


if __name__ == '__main__':
    while True:
        connection, address = server.accept()
        task = connection.recv(24).decode('utf-8')
        print(task)
        thread = threading.Thread(target=handle_connection, args=(connection, address, task))
        thread.start()

# import socket
# import struct
# import threading
#
#
# class Server(threading.Thread):
#     def __init__(self, host='127.0.0.1', port=6190):
#         super().__init__()
#         self.host = host
#         self.port = port
#         self.serverAddress = (self.host, self.port)
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.clientConnection = None
#         self.clientAddress = None
#         self.daemon = True
#
#     def run(self):
#         self.server.bind(self.serverAddress)
#         self.server.listen()
#         print('Server is listening')
#
#         while True:
#             self.clientConnection, self.clientAddress = self.server.accept()
#             thread = threading.Thread(target=self.handle_connection,
#                                       args=(self.clientConnection, self.clientAddress),
#                                       daemon=self.daemon)
#             thread.start()
#
#     def handle_connection(self):
#         print('Connected by', self.clientAddress)
#
#         sizeof_bytes = self.clientConnection.recv(4)
#         sizeof = struct.unpack('!I', sizeof_bytes)[0]
#         print(sizeof, "bytes received")
#
#         try:
#             filename = self.clientConnection.recv(24).decode('utf-8')[::-1]
#             self.clientConnection.send("File name received".encode('utf-8'))
#         except UnicodeDecodeError:
#             filename = "Unknown!"
#             self.clientConnection.send("File name not received".encode('utf-8'))
#
#         data = b""
#         while len(data) < sizeof:
#             packet = self.clientConnection.recv(sizeof - len(data))
#             if not packet:
#                 break
#             data += packet
#
#         status_of_file = ''
#         try:
#             with open('b' + filename, 'xb') as f:
#                 f.write(data)
#             status_of_file = 'File successfully write'
#         except FileExistsError:
#             with open('b' + filename + '(1)', 'xb') as f:
#                 f.write(data)
#             status_of_file = 'File name exists. File b{}(1) is created'.format(filename)
#         finally:
#             self.clientConnection.send(status_of_file.encode('utf-8'))
#             self.clientConnection.close()
#
#
# if __name__ == '__main__':
#     file_server = Server()
#     file_server.start()
