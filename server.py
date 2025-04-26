import socket

#host = socket.gethostbyname(socket.gethostname())
HOST = '192.168.18.14'

port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, port))

server.listen(5)
#unaccepted connections until 5

while True:

    communication_socket, address = server.accept()
    #waiting for connections
    print(f"Connected to {address}")

    message = communication_socket.recv(1024).decode('utf-8')
    #1024 bytes
    print(f"Message from client is: {message}")
    communication_socket.send(f"No te rindas ctm.".encode('utf-8'))
    communication_socket.close()
    print(f"Connection with {address} ended")





