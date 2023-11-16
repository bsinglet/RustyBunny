__author__  = 'Benjamin M. Singleton'
__date__    = '16 November 2023'
__version__ = '0.1.0'

import socket
import time

CONTROL_HOSTNAME = '127.0.0.1' #socket.gethostname()
CONTROL_PORT = 3003

def open_socket(hostname: str, port: int) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((hostname, port))
    server_socket.listen(5)
    return server_socket


def send_socket(client_socket: socket.socket, payload: str) -> None:
    """
    Sends the given message, padded out to 2048 bytes. Next improvement would
    be preceding it with a 4-byte header indicating the total message length.
    After that, some code to resend broken messages, but don't want to built
    this out too much yet as the real design will need to be able to
    dynamically switch to other control nodes as connections are lost/broken.
    """
    MSGLEN = 2048
    total_bytes_sent = 0
    encoded_message = payload.encode()
    encoded_message = encoded_message + (' ' * (MSGLEN - len(encoded_message))).encode()
    while total_bytes_sent < MSGLEN:
        bytes_sent = client_socket.send(encoded_message[total_bytes_sent:])
        if bytes_sent == 0:
            raise RuntimeError(f"Client socket connection broken while sending message {payload}")
        total_bytes_sent += bytes_sent
    print(f"Sent {total_bytes_sent} bytes to client")


def main():
    server_socket = open_socket(CONTROL_HOSTNAME, CONTROL_PORT)
    while True:
        (client_socket, client_address) = server_socket.accept()
        print(f"Received client node connection from {client_address}")
        time.sleep(5)
        print(f"Sending message to client node")
        send_socket(client_socket=client_socket, payload="Hello")
        send_socket(client_socket=client_socket, payload="quit")


if __name__ == '__main__':
    main()
