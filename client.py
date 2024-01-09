import socket
import struct
from time import sleep

HOST = '127.0.0.1'
PORT = 6190
addr = (HOST, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

print("Connected to server")


# Client PUT
def put(_filename):
    lenFileNameAsByte = len(_filename).to_bytes(4, 'little', signed=False)
    client.send(lenFileNameAsByte)
    print(f"Sent Over TCP: {lenFileNameAsByte}")
    client.send(_filename.encode())
    print(f"Sent Over TCP: {_filename}")
    print("Recived from Server: " + client.recv(26).decode())
    with open(_filename, 'rb') as f:
        _bytes = f.read()
        sizeof = len(_bytes)
    print(f"ReadFile {_filename}: Size {sizeof}")
    client.send(sizeof.to_bytes(16, 'little', signed=False))
    print("Sent Over TCP: Size of file")
    client.sendall(_bytes)
    print("Sent Over TCP: File Bytes")
    statusOfFile = client.recv(100).decode('utf-8')
    print(statusOfFile)


def get(_client, _filename, _path=''):
    _client.send(_filename.encode('utf-8'))
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


def doTask(_command):
    global client
    _task, _filename, _path = _command
    client.sendall(_task.encode('utf-8'))
    if _task == 'put':
        put(_filename)
    elif _task == 'get':
        get(client, _filename, _path)


while True:
    command = input('>>').split()
    print(command)
    if command[0] == 'exit':
        break
    else:
        doTask(command)

client.close()
