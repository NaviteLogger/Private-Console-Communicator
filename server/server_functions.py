from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os, socket, time, mysql.connector
from dotenv import load_dotenv
from threading import Thread

# Get the environment variables
load_dotenv()


# Connect to the MySQL database
def connect():
    # Connect to the database
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

    return connection


def generate_key_pair_for_client():
    # Generate an RSA key pair for the desired client
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()

    # Serialize the public key to send to the client
    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_key, serialized_public_key


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
            store_message(client_id, partner_id, encrypted_message)

            # Forward the message to the conversation partner
            forward_message(client_id, partner_id, encrypted_message)
