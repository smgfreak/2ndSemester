"""
    Script which listens for messages on a hardcoded port 8881

    @Author: orda
"""
import socket
import sys


def main():
    if len(sys.argv) > 1:
        port = sys.argv[1]
        int(port)
    else:
        port = 8881

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    my_socket.bind(('', port))

    print('listener started...')

    while True:
        message, address = my_socket.recvfrom(port)
        dmessage = message.decode('utf-8')  # Decode to utf-8
        print(f'received: {dmessage}, from: {address[0]}')


if __name__ == "__main__":
    main()
