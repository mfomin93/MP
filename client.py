# Control API Client

import socket

class Client:
    def __init__(self):
        self.ip = 'https://192.168.0.23'
        self.port = 80
        self.username = 'wattbox'
        self.password = 'SnapAV704'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print("Connecting on " + self.ip + " " + str(self.port))
        self.socket.settimeout(5)
        self.socket.connect((self.ip, self.port))
        self.socket.settimeout(None)

    def reconnect(self):
        print("Reconnecting on " + self.ip + " " + str(self.port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.socket.connect((self.ip, self.port))
        self.socket.settimeout(None)

    def send(self, data):
        print("TX: " + data)
        self.socket.sendall(data.encode())

    def timeout(self, timeout):
        self.socket.settimeout(timeout)

    def receive(self):
        buffer = ''
        while True:
            data = self.socket.recv(1024)
            if data:
                buffer += data.decode()
                print("RX: " + buffer)
                return buffer
            else:
                break

    def disconnect(self):
        print("Disconnecting on " + self.ip)
        self.socket.close()
