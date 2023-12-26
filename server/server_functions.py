from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import psycopg2, os
from dotenv import load_dotenv

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
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()

    # Serialize the public key to send to the client
    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_key, serialized_public_key


def store_active_connections(cursor, public_key, address, port):
    # Insert the public key, address and port of the client into the database
    cursor.execute(
        "INSERT INTO active_connections (public_key, address, port) VALUES (%s, %s, %s)",
        (public_key, address, port),
    )


def get_active_connections(cursor):
    # Get all active connections from the database
    cursor.execute("SELECT * FROM active_connections")

    # Fetch all the rows from the cursor
    active_connections = cursor.fetchall()

    return active_connections


def remove_active_connection(public_key):
    # Establish a connection to the database
    connection = connect()

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    # Remove the active connection from the database
    cursor.execute(
        "DELETE FROM active_connections WHERE public_key = %s", (public_key,)
    )

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
