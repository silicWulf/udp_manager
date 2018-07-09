import socket
import time


class DroneSocket:
    def __init__(self, hosting, to_host):
        dat = {vn: val for vn, val in locals().items() if val != self}
        for varname, host in dat.items():
            if not hasattr(host, "__getitem__"):  # test if iterable
                raise TypeError("'{}' must be iterable (tuple, list, ...)".format(varname))
        try:
            ip, port = hosting
            to_ip, to_port = to_host
        except ValueError as ve:
            raise ve

        self._udpserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._udpserver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._udpserver.bind((ip, port))

        self.to_ip, self.to_port = to_ip, to_port

    def send(self, data):
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(data, (self.to_ip, self.to_port))

    def recv(self, buffer):
        return self._udpserver.recvfrom(buffer)
