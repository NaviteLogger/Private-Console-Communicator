import server_functions, socket, dotenv, os

# Load the environment variables from the .env file
dotenv.load_dotenv()

# Connect to the database
cursor, connection = server_functions.connect_to_database()

# Create the desired tables:
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY,
        public_key TEXT,
        address TEXT,
        port INTEGER,
        partner_id INTEGER,
        FOREIGN KEY (partner_id) REFERENCES connections (id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        sender_id INTEGER,
        recipient_id INTEGER,
        message TEXT,
        FOREIGN KEY (sender_id) REFERENCES connections (id),
        FOREIGN KEY (recipient_id) REFERENCES connections (id)
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
