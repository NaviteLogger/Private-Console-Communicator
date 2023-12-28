from cryptography.hazmat.backends import default_backend
import os, sqlite3
from dotenv import load_dotenv

# Get the environment variables
load_dotenv()


# Connect to the SQLite database
def connect_to_database():
    # Connect to the SQLite database
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), "database", "database.db"))
    cursor = connection.cursor()

    return cursor, connection


def store_connection(public_key, address, port, cursor, connection):
    # Insert the public key, address and port of the client into the database
    cursor.execute(
        "INSERT INTO connections (public_key, address, port) VALUES (%s, %s, %s)",
        (public_key, address, port),
    )

    # Commit the changes to the database
    connection.commit()


def create_conversation(client_id, partner_id, cursor, connection):
    # Create a conversation between the client and the partner
    cursor.execute("UPDATE connections SET partner_id = ? WHERE id = ?", (partner_id, client_id))
    cursor.execute("UPDATE connections SET partner_id = ? WHERE id = ?", (client_id, partner_id))
    # Commit the changes to the database
    connection.commit()


def store_message(sender_id, recipient_id, message, cursor, connection):
    # Insert the message into the database
    cursor.execute(
        "INSERT INTO messages (sender_id, recipient_id, message) VALUES (%s, %s, %s)",
        (sender_id, recipient_id, message),
    )

    # Commit the changes to the database
    connection.commit()


def forward_message(sender_id, recipient_id, message, cursor, connection):
    # Forward the message to the recipient
    store_message(sender_id, recipient_id, message, cursor, connection)


def handle_client(client_socket, client_id, cursor, connection):
    # Receive the client's public key, address and port
    client_public_key = client_socket.recv(1024).decode()

    while True:
        # Receive encrypted messages from the client
        encrypted_message = client_socket.recv(1024)
        if not encrypted_message:
            break

        # If the message is a new conversation request, create a conversation between the client and the partner
        if encrypted_message.startswith(b"new_conversation"):
            partner_id = int(encrypted_message.split()[1].decode())
            create_conversation(client_id, partner_id, cursor, connection)
            store_connection(client_public_key, client_socket.getpeername()[0], client_socket.getpeername()[1], cursor, connection)

            # Notify the client about starting a new conversation
            client_socket.send(f"CONVERSATION_STARTED {partner_id}".encode())
        else:
            # Store the encrypted message in the database for forwarding
            cursor.execute("SELECT partner_id FROM connections WHERE id = ?", (client_id,))
            partner_id = cursor.fetchone()[0]
            store_message(client_id, partner_id, encrypted_message, cursor, connection)

            # Forward the message to the conversation partner
            forward_message(client_id, partner_id, encrypted_message, cursor, connection)
