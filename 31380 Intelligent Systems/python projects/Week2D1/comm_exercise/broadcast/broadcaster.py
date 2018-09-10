"""
    Script which broadcasts random integers to a hardcoded port 8881

    @Author: orda
"""

import socket
import random
import time
import sys


def main():
    if len(sys.argv) > 1:
        port = sys.argv[1]
        int(port)
    else:
        port = 8881

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Allow reuse in case we exited ungracefully
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('broadcaster started...')

    while True:
        number = random.randint(1, 101)
        print("sending: ", number)
        my_socket.sendto((f'Number: {number}').encode('utf-8'), ('<broadcast>', 8881))
        time.sleep(1)

    my_socket.close()


if __name__ == "__main__":
    main()
