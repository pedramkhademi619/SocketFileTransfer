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


def handle_connection(conn, _addr):
    # Critical Session
    mutex = threading.Lock()
    mutex.acquire()
    print('Connected by', _addr)
    sizeof_bytes = conn.recv(4)
    sizeof = struct.unpack('!I', sizeof_bytes)[0]
    print(sizeof)
    print(sizeof, "bytes received")
    try:
        filename = conn.recv(24).decode('utf-8')[::-1]
        sleep(1)
        conn.send("server>>File name received".encode('utf-8'))

    except UnicodeDecodeError:
        filename = "Unknown!"
        conn.send("server>>File name not received".encode('utf-8'))

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
        statusOfFile = 'server>>File successfully write in Server:{}'.format(os.path.abspath('b' + filename))
    except FileExistsError:
        _filename = 'b' + filename
        with open('1' + _filename, 'xb') as f:
            f.write(data)
        statusOfFile = 'server>>File name exists. File 1b{} is saved in Server:{}.'.format(filename, os.path.abspath('b' + filename))
    finally:
        conn.send(statusOfFile.encode('utf-8'))
        conn.close()
        mutex.release()


if __name__ == '__main__':
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_connection, args=(connection, address))
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
