import socket, config, string, random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def read_config():
    # Read the config file
    server_ip = config.SERVER_IP
    server_port = int(config.SERVER_PORT) if config.SERVER_PORT is not None else None

    return server_ip, server_port


def connect_to_server():
    # Create a socket to connect to the server
    server_ip, server_port = read_config()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    return client_socket


def generate_conversation_id(length):
    # Generate a unique string for the other user to join the conversation
    conversation_id = "".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(length))

    return conversation_id


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


def send_message(sock, message, recipient_public_key):
    # Encrypt the message to be sent with the server's provi
    encrypted_message = recipient_public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

    # Send the encrypted message to the server
    sock.send(encrypted_message)
