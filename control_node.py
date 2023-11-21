__author__  = 'Benjamin M. Singleton'
__date__    = '16 November 2023'
__version__ = '0.1.1'

import binascii
import socket
import time

CONTROL_HOSTNAME = '127.0.0.1'
CONTROL_PORT = 3003

def open_socket(hostname: str, port: int) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((hostname, port))
    server_socket.listen(5)
    return server_socket


def send_socket(client_socket: socket.socket, payload: bytes, message_length: int) -> None:
    """
    Sends the given message, padded out to message_length bytes.
    """
    total_bytes_sent = 0
    encoded_message = payload + (' ' * (message_length - len(payload))).encode()
    while total_bytes_sent < message_length:
        bytes_sent = client_socket.send(encoded_message[total_bytes_sent:])
        if bytes_sent == 0:
            raise RuntimeError(f"Client socket connection broken while sending message {payload}")
        total_bytes_sent += bytes_sent
    print(f"Sent {total_bytes_sent} bytes to client")


def send_packet(client_socket: socket.socket, payload: str) -> None:
    # send the 4-byte length indicator
    send_socket(client_socket=client_socket, payload=int(len(payload.encode())).to_bytes(4), message_length=4)
    time.sleep(1)
    send_socket(client_socket=client_socket, payload=payload.encode(), message_length=len(payload.encode()))
    time.sleep(1)
    # print(f"Sending checksum {binascii.crc32(payload.encode())}")
    # send_socket(client_socket=client_socket, payload=binascii.crc32(payload.encode()).to_bytes(), message_length=4)
    # time.sleep(1)


def main():
    server_socket = open_socket(CONTROL_HOSTNAME, CONTROL_PORT)
    while True:
        (client_socket, client_address) = server_socket.accept()
        print(f"Received client node connection from {client_address}")
        time.sleep(0.5)
        # print(f"Sending message to client node")
        send_packet(client_socket=client_socket, payload="Hello")
        time.sleep(0.5)
        send_packet(client_socket=client_socket, payload="quit")


if __name__ == '__main__':
    main()
