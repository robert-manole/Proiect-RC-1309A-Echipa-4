import socket
import Packets as packets
import threading
import time

class Client:

    def __init__(self, id, keep_alive):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = id
        self.keep_alive_start = 0
        self.keep_alive = keep_alive

    def getId(self):
        return self.__id

    def reset_keep_alive_start(self):
        self.keep_alive_start = int(time.time())

    def connect(self, username, password):
        self.s.connect(('127.0.0.1', 6000))

        packet = packets.CONNECT(self.__id, username, password, self.keep_alive)
        packet = packet.parse()

        self.s.sendall(packet)

        self.reset_keep_alive_start()
        threading.Thread(target=self.keep_alive_thread).start()

        msg = self.s.recv(1024)
        print(msg)

    def publish(self, topic_name, qos_lvl):
        packet = packets.PUBLISH(topic_name, qos_lvl)
        packet = packet.parse()

        self.s.sendall(packet)
        self.reset_keep_alive_start()

        # if not self.recv_thread.is_alive():
        #     self.recv_thread.start()

        # msg = self.s.recv(1024)
        # print(msg)

    def subscribe(self, topic_name, text_msg, text_subs):

        packet = packets.SUBSCRIBE(topic_name)
        packet = packet.parse()

        self.s.sendall(packet)
        self.reset_keep_alive_start()

        subs = text_subs.get('1.0', 'end')

        if topic_name not in subs:
            text_subs.config(state='normal')
            text_subs.insert('end', topic_name + '\n')
            text_subs.config(state='disabled')

        recv_thread = threading.Thread(target=self.receive_msg, args=(self.s, text_msg))
        if not recv_thread.is_alive():
            recv_thread.start()

        # msg = self.s.recv(1024)
        # print(msg)

    def unsubscribe(self, topic_name, text_subs):
        packet = packets.UNSUBSCRIBE(topic_name)
        packet = packet.parse()

        self.s.sendall(packet)
        self.reset_keep_alive_start()

        subs = text_subs.get('1.0', 'end')
        subs_arr = subs.split('\n')
        idx = subs_arr.index(topic_name)
        text_subs.config(state='normal')
        text_subs.delete(str(idx + 1) + '.0', str(idx + 1) + '.end+1c')
        text_subs.config(state='disabled')

        # msg = self.s.recv(1024)
        # print(msg)

    def disconnect(self):
        packet = packets.DISCONNECT()
        packet = packet.parse()

        self.s.sendall(packet)
        # msg = self.s.recv(1024)
        # print(msg)

    def pingreq(self):
        packet = packets.PINGREQ()
        packet = packet.parse()

        self.s.sendall(packet)
        # msg = self.s.recv(1024)
        # print(msg)

    def receive_msg(self, s, text_msg):
        while 1:
            msg = s.recv(4096)
            if msg:
                print(msg)
                if msg[0] == 0x34 or msg[0] == 0x32 or msg[0] == 0x30: # publish pack

                    if msg[1] > 127:
                        offset = 5
                    else:
                        offset = 4

                    topic_name_len = int(msg[offset - 1])
                    topic_name = msg[offset: offset + topic_name_len]
                    topic_message = msg[offset + topic_name_len + 4 : -1]

                    text_msg.config(state='normal')
                    text_msg.insert('1.0', str(topic_name, encoding='ascii') + ":\n" + str(topic_message, encoding='ascii') + '\n\n')
                    text_msg.config(state='disabled')

    def keep_alive_thread(self):
        while 1:
            if int(time.time()) - self.keep_alive_start >= self.keep_alive:
                self.pingreq()
                self.reset_keep_alive_start()
            time.sleep(1)

