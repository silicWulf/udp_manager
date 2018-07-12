import socket
import time


class DroneSocket:
    def __init__(self, hosting, to_host, udp=True, is_hosting=True):
        dat = {vn: val for vn, val in locals().items() if val != self}
        for varname, host in dat.items():
            if 'host' in varname:
                if not hasattr(host, "__getitem__"):  # test if iterable
                    raise TypeError("'{}' must be iterable (tuple, list, ...)".format(varname))
        try:
            ip, port = hosting
            to_ip, to_port = to_host
        except ValueError as ve:
            raise ve

        self.to_ip, self.to_port = to_ip, to_port

        if self.udp is True:
            self._udpserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._udpserver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._udpserver.bind((ip, port))

        else:
            if is_hosting is False:
                self._clienttcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self._clienttcp.connect((self.to_ip, self.to_port))
                except Exception as e:
                    print("Unable to connect!")
                    raise e
            else:
                self._servertcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._servertcp.bind((ip, port))
                self._servertcp.listen(1)
                print("waiting for connection...")
                sock, addr = self._servertcp.accept()
                print("connection received!")
                self._tcpout = sock

    def send(self, data):
        if self.udp is True:
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(data, (self.to_ip, self.to_port))
        else:
            if self.is_hosting:
                self._servertcp.sendall(data)
            else:
                self._clienttcp.send(data)

    def recv(self, buffer):
        if self.udp is True:
            return self._udpserver.recvfrom(buffer)
        else:
            if not self.is_hosting:
                return self._clienttcp.recv(buffer)
            else:
                return self._tcpout.recv(buffer)
