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
    print(client.recv(26).decode())
    with open(_filename, 'rb') as f:
        _bytes = f.read()
        sizeOfFile = len(_bytes)
    print(f"ReadFile {_filename}: Size {sizeOfFile}")
    client.send(sizeOfFile.to_bytes(16, 'little', signed=False))
    print("Sent Over TCP: Size of file")
    client.sendall(_bytes)
    print("Sent Over TCP: File Bytes")
    statusOfFile = client.recv(100).decode('utf-8')
    print(statusOfFile)


def get(_filename, _path=''):
    lenFileNameAsByte = (len(_filename)).to_bytes(4, 'little', signed=False)
    client.send(lenFileNameAsByte)
    print(f"Sent Over TCP: lenFileName: {len(_filename)}")
    client.send(_filename.encode('utf-8'))
    print(f'Sent Over TCP: FileName: {_filename}')
    print(client.recv(26).decode('utf-8'))
    sizeOfData = int.from_bytes(client.recv(4), 'little', signed=False)
    print(f"Received Over TCP: size of data: {sizeOfData}")
    data = client.recv(sizeOfData)
    print(f"Received Over TCP: data")
    try:
        with open(_path + '/' + _filename, 'xb') as f:
            f.write(data)
    except FileExistsError:
        print("File already exists")


# To Do: Implementation of checking file availability by file name.
# If the file exists, input will be taken again.

def doTask(_command):
    _task, _filename, _path = _command
    client.sendall(_task.encode('utf-8'))
    if _task == 'put':
        put(_filename)
    elif _task == 'get':
        get(_filename, _path)


while True:
    command = input('>>').split()
    if command[0] == 'exit':
        break
    else:
        doTask(command)
client.close()
