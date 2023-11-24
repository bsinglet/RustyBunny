__author__  = 'Benjamin M. Singleton'
__date__    = '16 November 2023'
__version__ = '0.1.1'

import time
from networking import open_socket, send_packet

CONTROL_HOSTNAME = '127.0.0.1'
CONTROL_PORT = 3003


def main():
    send_socket = open_socket(CONTROL_HOSTNAME, CONTROL_PORT)
    while True:
        (client_socket, client_address) = send_socket.accept()
        print(f"Received client node connection from {client_address}")
        time.sleep(0.5)
        # print(f"Sending message to client node")
        send_packet(client_socket=client_socket, payload="Hello")
        time.sleep(0.5)
        send_packet(client_socket=client_socket, payload="sh powershell.exe ls")
        time.sleep(0.5)
        send_packet(client_socket=client_socket, payload="quit")


if __name__ == '__main__':
    main()
