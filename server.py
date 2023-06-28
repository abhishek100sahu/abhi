import socket
import threading

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

app = Dash(__name__)

# header size of 64-bits to be tranffered
HEADER = 64
PORT = 5050
# getting IP address of the server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# defining specific format on which data should tranfer
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISSCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (type, method)

# port binding
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] \nNode : {msg[:2]} \nTemp: {msg[2:10]}")
            conn.send("Message recieved".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")


print("[Starting] Server is starting...")

start()

# flask application
app.layout = html.Div([
    html.H1(children='Title', style={'textAlign':'center'}),
    dcc.Graph
])
