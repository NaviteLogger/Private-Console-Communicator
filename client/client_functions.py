import socket
import threading
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def send_message(sock, message, recipient_public_key):
    # Encrypt the message to be sent with the server's provi
    encrypted_message = recipient_public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

    # Send the encrypted message to the server
    sock.send(encrypted_message)
