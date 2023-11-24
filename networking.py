import binascii
import socket
import time


def connect_to_control_port(hostname: str, port: int) -> socket.socket:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((hostname, port))
    return my_socket


def receive_message(my_socket: socket.socket, message_length: int) -> bytes:
    """
    Borrowed from:
    https://docs.python.org/3/howto/sockets.html
    """
    chunks = []
    bytes_recd = 0
    while bytes_recd < message_length:
        chunk = my_socket.recv(min(message_length - bytes_recd, 2048))
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)


def get_command(my_socket: socket.socket) -> str:
    message_length = int.from_bytes(receive_message(my_socket=my_socket, message_length=4))
    # print(f"Received packet header with message length {message_length}")
    message = receive_message(my_socket=my_socket, message_length=message_length)
    # print(f"Received message {message} of length {len(message)}")
    """checksum = int.from_bytes(receive_message(my_socket=my_socket, message_length=4))
    if binascii.crc32(message.encode()) != checksum:
        raise RuntimeError(f"Received message over the wire with checksum {binascii.crc32(message.encode())}, but expected checksum {checksum}")"""
    return message.decode()


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

