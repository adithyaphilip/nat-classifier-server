import socket
import threading
from time import sleep

__IP1__ = input("Enter first IP\n")
__IP2__ = input("Enter second IP\n")
__PORT_ALLOC_0__ = 2000
__PORT_ALLOC_1__ = 2001
__PORT_ALLOC_2__ = 2002
__PORT_FIL0__ = 4000
__PORT_FIL1__ = 4001
__PORT_FIL2__ = 4002

__UDP_BUF_SIZE__ = 2048


def get_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    return sock


def start_stun(sock: socket.socket):
    while True:
        bytes, addr = sock.recvfrom(__UDP_BUF_SIZE__)
        sock.sendto(str(addr[1]).encode("utf-8"), addr)


def main():
    sock1 = get_socket(__IP1__, __PORT1__)
    sock2 = get_socket(__IP1__, __PORT2__)
    sock3 = get_socket(__IP2__, __PORT3__)
    threading.Thread(group=None, target=start_stun, args=(sock2,)).start()
    threading.Thread(group=None, target=start_stun, args=(sock3,)).start()
    while True:
        bytes, addr = sock1.recvfrom(__UDP_BUF_SIZE__)
        print(addr)
        sock1.sendto(str(addr[0]).encode("utf-8"), addr)
        sock2.sendto(str(addr[0]).encode("utf-8"), addr)
        sock3.sendto(str(addr[0]).encode("utf-8"), addr)


main()
