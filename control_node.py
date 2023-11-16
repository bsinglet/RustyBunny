__author__  = 'Benjamin M. Singleton'
__date__    = '16 November 2023'
__version__ = '0.1.0'

import socket

CONTROL_HOSTNAME = socket.gethostname()
CONTROL_PORT = 3003

def open_socket(hostname: str, port: int) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((hostname, port))
    server_socket.listen(5)
    return server_socket


def send_socket(client_socket: socket.socket, payload: str):
    pass


def main():
    server_socket = open_socket(CONTROL_HOSTNAME, CONTROL_PORT)
    while True:
        (client_socket, client_address) = server_socket.accept()


if __name__ == '__main__':
    main()
