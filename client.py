import socket
import random
import time

# header size of 64-bits to be tranffered
HEADER = 64
PORT = 5050
# getting IP address of the server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISSCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (type, method)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_lenght = str(msg_length).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)

while True:
    send(str(random.randint(10000000000000000,999999999999999999)))
    time.sleep(2)


send(DISCONNECT_MESSAGE)