import socket
import configparser
import threading
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def read_config():
    # Read the client configuration file
    config = configparser.ConfigParser()
    config.read("config.ini")

    server_ip = config["Server"]["server_ip"]
    server_port = int(config["Server"]["server_port"])

    return server_ip, server_port


def connect_to_server():
    # Create a socket to connect to the server
    server_ip, server_port = read_config()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    return client_socket


def send_message(sock, message, recipient_public_key):
    # Encrypt the message to be sent with the server's provi
    encrypted_message = recipient_public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

    # Send the encrypted message to the server
    sock.send(encrypted_message)
