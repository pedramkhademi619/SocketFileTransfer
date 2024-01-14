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


def get(_conn: socket.socket):
    lenFileName = int.from_bytes(_conn.recv(4), 'little', signed=False)  # getting an integer sized value over socket
    print(f"Received Over TCP: lenFileName: {lenFileName}")
    try:
        filename = _conn.recv(lenFileName).decode()
        print(f'Received Over TCP: FileName: {filename}')
        _conn.send("Server>>File name received".encode())
    except UnicodeDecodeError:
        filename = "Unknown!"
    data_length = int.from_bytes(_conn.recv(16), 'little', signed=False)
    print(f"Received Over TCP: data_length: {data_length}")
    data = _conn.recv(data_length)
    statusOfFile = ''
    try:
        with open('b' + filename, 'xb') as f:
            f.write(data)
        statusOfFile = f'server>>File successfully write in Server:{os.path.abspath("b" + filename)}'
    except FileExistsError:
        _filename = 'b' + filename
        with open('1' + _filename, 'xb') as f:
            f.write(data)
        statusOfFile = 'server>>File name exists. File 1b{} is saved in Server:{}.'.format(filename, os.path.abspath(
            'b' + filename))
    finally:
        _conn.send(statusOfFile.encode())


def put(_conn):
    lenFileName = int.from_bytes(_conn.recv(4), 'little', signed=False)  # getting an integer sized value over socket
    print(f"Received Over TCP: lenFileName: {lenFileName}")
    filename = _conn.recv(lenFileName).decode('utf-8')
    _conn.send("server>>File name received".encode('utf-8'))

    with open(filename, 'rb') as f:
        _bytes = f.read()
        sizeOfFile = len(_bytes).to_bytes(4, 'little')
    print(f"ReadFile {filename}")
    _conn.send(sizeOfFile)
    print("Sent Over TCP: Size of file")
    _conn.sendall(_bytes)
    print("Sent Over TCP: File Bytes")


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
        if task == 'exit':
            connection.close()
        print(task)
        thread = threading.Thread(target=handle_connection, args=(connection, address, task))
        thread.start()
