from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import psycopg2, os, socket, time
from dotenv import load_dotenv
from threading import Thread

# Get the environment variables
load_dotenv()


# Connect to the PostgreSQL database
def connect():
    try:
        connection = psycopg2.connect(
            user=os.getenv("POSTGRESQL_DB_USER"),
            password=os.getenv("POSTGRESQL_DB_PASSWORD"),
            host=os.getenv("POSTGRESQL_DB_HOST"),
            port=os.getenv("POSTGRESQL_DB_PORT"),
            database=os.getenv("POSTGRESQL_DB_NAME"),
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL database, error: ", error)


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


def store_connection(cursor, connection, public_key, address, port):
    # Insert the public key, address and port of the client into the database
    cursor.execute(
        "INSERT INTO active_connections (public_key, address, port) VALUES (%s, %s, %s)",
        (public_key, address, port),
    )

    # Commit the changes to the database
    connection.commit()


def create_chat_room(cursor, connection):
    # Generate a unique chat_room_id
    chat_room_id = "chat_" + str(hash(socket.gethostname() + str(time.time())))

    # Create a new chat room in the database
    # Insert the chat room into the database
    cursor.execute("INSERT INTO chat_rooms (chat_room_id) VALUES (%s)", (chat_room_id,))

    # Commit the changes to the database
    connection.commit()

    return chat_room_id


def join_chat_room(client_id, chat_room_id, cursor, connection):
    # Insert the client into the chat room
    cursor.execute(
        "INSERT INTO user_chat_rooms (client_id, chat_room_id) VALUES (%s, %s)",
        (client_id, chat_room_id),
    )

    # Commit the changes to the database
    connection.commit()


def store_message(sender_id, chat_room_id, message, cursor, connection):
    # Insert the message into the database
    cursor.execute(
        "INSERT INTO messages (sender_id, chat_room_id, message) VALUES (%s, %s, %s)",
        (sender_id, chat_room_id, message),
    )

    # Commit the changes to the database
    connection.commit()
