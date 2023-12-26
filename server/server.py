import server_functions
import socket

# Connect to the database
connection = server_functions.connect()

# Create a cursor to perform database operations
cursor = connection.cursor()

# Create the table to store active connections
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY,
        address TEXT,
        port INTEGER
    )
"""
)

# Commit the changes to the database
connection.commit()

# Close the cursor and connection for now
cursor.close()
connection.close()

# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 5555))
server_socket.listen(5)

print("Server is listening for incoming connections...")

while True:
    # Accept an incoming connection from a client
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established!")
