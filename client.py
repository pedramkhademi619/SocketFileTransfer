import socket
import struct
from time import sleep

HOST = '127.0.0.1'
PORT = 6190
addr = (HOST, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

print("Connected to server")


def put(_filename):
    with open(filename, 'rb') as f:
        _bytes = f.read()
        sizeof = len(_bytes)
    client.send(struct.pack("!I", sizeof))
    client.send(filename[::-1].encode('utf-8'))
    client.sendall(_bytes)

    statusOfFile = client.recv(100).decode('utf-8')
    print(statusOfFile)


def get(_client, _path, _filename):
    _client.send(_filename[::-1].encode('utf-8'))
    print(_client.recv(28).decode('utf-8'))
    sizeof = _client.recv(4)
    sizeof = struct.unpack("!I", sizeof)[0]
    print('sizeof ' + 'is ' + str(sizeof))
    data = b""
    while len(data) < sizeof:
        packet = client.recv(sizeof - len(data))
        if not packet:
            break
        data += packet
    try:
        with open(_path + '/' + _filename, 'xb') as f:
            f.write(data)
    except FileExistsError:
        print("File already exists")


path = 'D:\\python\\socket\\first'


def doTask(_task, _path, _filename):
    global client
    client.sendall(_task.encode('utf-8'))
    if _task == 'put':
        put(filename)
    elif _task == 'get':
        get(client, _path, _filename)


task, filename, _path = input(">>").split()
doTask(task, _path, filename)

client.close()
