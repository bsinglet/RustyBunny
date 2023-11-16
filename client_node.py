__author__  = 'Benjamin M. Singleton'
__date__    = '16 November 2023'
__version__ = '0.1.0'

import socket
import yaml


def load_config(filename: str) -> dict:
    with open(filename, 'r') as my_file:
        config = yaml.safe_load(my_file)
    return config


def connect_to_control_port(hostname: str, port: int) -> socket.socket:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((hostname, port))
    return my_socket


def get_command(my_socket: socket.socket) -> str:
    """
    Borrowed from:
    https://docs.python.org/3/howto/sockets.html
    """
    MSGLEN = 2048
    chunks = []
    bytes_recd = 0
    while bytes_recd < MSGLEN:
        chunk = my_socket.recv(min(MSGLEN - bytes_recd, 2048))
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks).decode()


def parse_command(command: str) -> list:
    return command.strip().split(' ')


def run_command(command: list) -> bool:
    match command:
        # necessary
        case ["download", *files]:
            print(f"Downloading " + ', '.join(files) + ".")
        # necessary
        case ["sh", *commands]:
            print(f"Running command on target: " + ', '.join(commands) + ".")
        case ["quit", *extra]:
            print(f"Received the [quit, extra] command, ending client node.")
            return False
        # fun
        case ["ddos", *targets]:
            print(f"DDoSing targets: " + ', '.join(targets) + ".")
        # stretch goals
        case ["suicide"]:
            print(f"Committing self-end, uninfecting host and clearing tracks.")
        # stretch goals
        case ["migrate", pid]:
            print(f"Migrating from current process to {pid}.")
        # easter eggs
        case ["baby", "shark"]:
            print("Playing an annoyingly catchy song.")
        # convenience functions
        case ["ls", *files]:
            print(f"Listing files " + ", ".join(files) + ".")
        case ["cat", *files]:
            print(f"Catting files " + ", ".join(files) + ".")
        case ['cd', directory]:
            print(f"Changing directory to {directory}.")
        case x:
            print(f"Unknown command: {x}")
    return True


def main():
    config = load_config('client_config.yml')
    control_hostname = config['control_node']['address']
    control_port = config['control_node']['port']
    my_socket = connect_to_control_port(hostname=control_hostname, port=control_port)
    print(f"Connected to control node at {control_hostname}:{control_port}")
    while True:
        # print("Receiving a command")
        command = get_command(my_socket)
        # print(f"Received command {command}")
        command = parse_command(command)
        if not run_command(command):
            break


if __name__ == '__main__':
    main()
