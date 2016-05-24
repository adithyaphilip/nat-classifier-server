import socket
import threading

IP1 = input("Enter first IP\n")
IP2 = input("Enter second IP\n")

IP_ORDER = (IP1, IP1, IP2)
PORTS_ALLOC = (2000, 2001, 2002)
PORTS_FILTER = (3000, 3001, 3002)

__UDP_BUF_SIZE__ = 2048


def get_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    return sock


def start_stun(sock: socket.socket):
    while True:
        b, addr = sock.recvfrom(__UDP_BUF_SIZE__)
        sock.sendto(str(addr[1]).encode("utf-8"), addr)


def start_alloc_check():
    socks = [get_socket(*addr) for addr in zip(IP_ORDER, PORTS_ALLOC)]
    for sock in socks:
        threading.Thread(group=None, target=start_stun, args=(sock,)).start()


def start_filtering_check():
    socks = [get_socket(*addr) for addr in zip(IP_ORDER, PORTS_FILTER)]
    while True:
        b, addr = socks[0].recvfrom(__UDP_BUF_SIZE__)
        print(addr)
        for sock in socks:
            sock.sendto(str(addr[1]).encode("utf-8"), addr)


def main():
    t_list = [threading.Thread(group=None, target=func) for func in (start_filtering_check, start_alloc_check)]
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
        print(str(t), "has stopped! :O")


main()
