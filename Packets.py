from abc import ABC, abstractmethod
from OS_Information import getMessageInstanceByTopicName
packetFixedHeader = {
    'CONNECT': b'\x10',
    'DISCONNECT': b'\xE0',
    'PUBLISH': b'\x32',
    'SUBSCRIBE': b'\x82',
    'UNSUBSCRIBE': b'\xA2',
    'PINGREQ': b'\xC0',
}


class Packet(ABC):
    @abstractmethod
    def parse(self):
        pass

class CONNECT(Packet):

    def __init__(self, id, username, password, keep_alive):

        self.packetPayload = {
            'client_id': str(id),
            'will_topic': 'CpuInfo',
            'will_message': '  Din cauza unei erori un alt client a fost deconectat',
            'username': username,
            'password': password
        }
        self.packetVariableHeader = {
            'protocol_name': "MQTT",
            'version': b'\x04',
            'connect_flags': b'\xf6',
            'keep_alive': b'\x00' + bytes(chr(keep_alive), encoding='ascii'),
        }

    def parse(self):
        packet = bytearray()

        packet += packetFixedHeader['CONNECT']

        variable_header = b'\x00'
        variable_header += bytes([len(self.packetVariableHeader['protocol_name'])])
        variable_header += self.packetVariableHeader['protocol_name'].encode('UTF-8')
        variable_header += self.packetVariableHeader['version']
        variable_header += self.packetVariableHeader['connect_flags']
        variable_header += self.packetVariableHeader['keep_alive']

        payload = b'\x00'
        payload += bytes([len(self.packetPayload['client_id'])])
        payload += self.packetPayload['client_id'].encode('UTF-8')
        payload += b'\x00'
        payload += bytes([len(self.packetPayload['will_topic'])])
        payload += self.packetPayload['will_topic'].encode('UTF-8')
        payload += b'\x00'
        payload += bytes([len(self.packetPayload['will_message'])])
        payload += self.packetPayload['will_message'].encode('UTF-8')
        payload += b'\x00'
        payload += bytes([len(self.packetPayload['username'])])
        payload += self.packetPayload['username'].encode('UTF-8')
        payload += b'\x00'
        payload += bytes([len(self.packetPayload['password'])])
        payload += self.packetPayload['password'].encode('UTF-8')
        variable_header += payload

        packet_length = bytes([len(variable_header)])
        packet += packet_length
        packet += variable_header

        return packet

class DISCONNECT(Packet):
    def parse(self):
        packet = bytearray()

        packet += packetFixedHeader['DISCONNECT']

        packet += b'\x00'  #remaining length

        return packet

class PUBLISH(Packet):

    def __init__(self, topic_name):

        os_info = getMessageInstanceByTopicName(topic_name)

        self.packetPayload = {
            'message': os_info.get_info()
        }
        self.packetVariableHeader = {
            'topic_name': topic_name,
            'packetIdentifier': b'\x00\x0a'
        }

    def parse(self):
        packet = bytearray()
        variable_header = bytearray()
        packet += packetFixedHeader['PUBLISH']

        variable_header += b'\x00'
        variable_header += bytes([len(self.packetVariableHeader['topic_name'])])
        variable_header += self.packetVariableHeader['topic_name'].encode('UTF-8')
        variable_header += self.packetVariableHeader['packetIdentifier']

        if len(self.packetPayload['message']) >= 256:
            len_msg = int(len(self.packetPayload['message']))
            rem = len_msg % 256
            div = len_msg / 256
            payload = bytes([int(div)])
            payload += bytes([rem])
        else:
            payload = b'\x00'
            payload += bytes([len(self.packetPayload['message'])])

        payload += self.packetPayload['message'].encode('UTF-8')
        variable_header += payload

        packet_length = len(variable_header)

        if packet_length > 127:
            rem = packet_length % 128
            div = packet_length / 128
            rem = rem + 128
            byte1 = bytes([rem])
            byte2 = bytes([int(div)])

            packet += byte1
            packet += byte2
        else:
            packet += bytes([packet_length])

        packet += variable_header
        print(packet)
        return packet

class SUBSCRIBE(Packet):

    def __init__(self, topic_name):

        self.packetPayload = {
            'Topic_name': topic_name,
            'req_QoS': b'\x02'
        }
        self.packetVariableHeader = {
            'packetIdentifier': b'\x00\x0b'
        }

    def parse(self):
        packet = bytearray()

        packet += packetFixedHeader['SUBSCRIBE']

        # variable_header = b'\x00'
        variable_header = self.packetVariableHeader['packetIdentifier']

        payload = b'\x00'
        payload += bytes([len(self.packetPayload['Topic_name'])])
        payload += self.packetPayload['Topic_name'].encode('UTF-8')
        payload += self.packetPayload['req_QoS']

        variable_header += payload

        packet_length = bytes([len(variable_header)])
        packet += packet_length
        packet += variable_header

        return packet

class UNSUBSCRIBE(Packet):


    def __init__(self, topic_name):
        self.topic_name = topic_name

        self.packetVariableHeader = {
            'packetIdentifier': b'\x00\x0b'
        }
        self.packetPayload = {
            'Topic_name': self.topic_name,
        }

    def parse(self):
        packet = bytearray()

        packet += packetFixedHeader['UNSUBSCRIBE']

        # variable_header = b'\x00'
        variable_header = self.packetVariableHeader['packetIdentifier']

        payload = b'\x00'
        payload += bytes([len(self.packetPayload['Topic_name'])])
        payload += self.packetPayload['Topic_name'].encode('UTF-8')

        variable_header += payload

        packet_length = bytes([len(variable_header)])
        packet += packet_length
        packet += variable_header

        return packet


class PINGREQ(Packet):
    def parse(self):
        packet = bytearray()

        packet += packetFixedHeader['PINGREQ']

        packet += b'\x00'  # remaining length

        return packet

