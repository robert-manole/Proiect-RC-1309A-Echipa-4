import socket
import Packets as packets
import threading


class Client:

    def __init__(self, id):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_thread = threading.Thread(target=self.receive_msg, args=(self.s,))
        self.__id = id

    def getId(self):
        return self.__id

    def connect(self, username, password):
        self.s.connect(('127.0.0.1', 6000))

        packet = packets.CONNECT(self.__id, username, password)
        packet = packet.parse()

        self.s.sendall(packet)
        msg = self.s.recv(1024)
        print(msg)

    def publish(self, topic_name):
        packet = packets.PUBLISH(topic_name)
        packet = packet.parse()

        self.s.sendall(packet)

        if not self.recv_thread.is_alive():
            self.recv_thread.start()

        # msg = self.s.recv(1024)
        # print(msg)

    def subscribe(self, topic_name):
        packet = packets.SUBSCRIBE(topic_name)
        packet = packet.parse()

        self.s.sendall(packet)

        if not self.recv_thread.is_alive():
            self.recv_thread.start()

        # msg = self.s.recv(1024)
        # print(msg)

    def unsubscribe(self):
        packet = packets.UNSUBSCRIBE()
        packet = packet.parse()

        self.s.sendall(packet)
        msg = self.s.recv(1024)
        print(msg)

    def disconnect(self):
        packet = packets.DISCONNECT()
        packet = packet.parse()

        self.s.sendall(packet)
        msg = self.s.recv(1024)
        print(msg)

    def pingreq(self):
        packet = packets.PINGREQ()
        packet = packet.parse()

        self.s.sendall(packet)
        msg = self.s.recv(1024)
        print(msg)

    def receive_msg(self, s):
        while 1:
            msg = s.recv(4096)
            if msg:
                print(msg)


