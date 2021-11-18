import socket
import Packets as packets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client:

    def __init__(self, id):
        self.__id = id

    def connect(self):
        s.connect(('127.0.0.1', 5000))

        packet = packets.CONNECT()
        packet = packet.parse()

        s.sendall(packet)
        msg = s.recv(1024)
        print(msg)


client = Client(1)
client.connect()

