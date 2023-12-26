import server_functions
import socket


# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 5555))
server_socket.listen(5)

print("Server is listening for incoming connections...")

while True:
    # Accept an incoming connection from a client
    client_socket, address = server_socket.accept()
