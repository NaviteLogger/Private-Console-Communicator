from db_connection import connect
import socket

# Establish a connectio to the database
connection = connect()

# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 5555))
server_socket.listen(5)
