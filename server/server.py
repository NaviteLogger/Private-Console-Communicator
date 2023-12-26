import server_functions
import socket

# Connect to the database
connection = server_functions.connect()

# Create a cursor to perform database operations
cursor = connection.cursor()

# Create the desired tables:
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY,
        address TEXT,
        port INTEGER,
        char_room_id TEXT,
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXIST messages (
        id INTEGER PRIMARY KEY,
        sender_id INTEGER,
        chat_room_id TEXT,
        message TEXT,
        FOREIGN KEY (sender_id) REFERENCES connections (id),
    )"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS chat_rooms (
        id INTEGER PRIMARY KEY,
        chat_room_id TEXT,
    )"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user_chat_rooms (
        user_id INTEGER,
        chat_room_id TEXT,
        FOREIGN KEY (user_id) REFERENCES connections (id),
        FOREIGN KEY (chat_room_id) REFERENCES chat_rooms (id),
        )"""
)

# Commit the changes to the database
connection.commit()

# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 5555))
server_socket.listen(5)

print("Server is listening for incoming connections...")

while True:
    # Accept an incoming connection from a client
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established!")
