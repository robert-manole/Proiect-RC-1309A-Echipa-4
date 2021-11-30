from abc import ABC, abstractmethod

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
    packetPayload = {
        'client_id': bytearray(),
        'will_topic': bytearray(),
        'will_message': bytearray(),
        'username': "",
        'password': ""
    }
    packetVariableHeader = {
        'protocol_name': "MQTT",
        'version': b'\x04',
        'connect_flags': b'\x02',
        'keep_alive': b'\x00\x05',
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
        payload += bytes([len(self.packetPayload['username'])])
        payload += self.packetPayload['username'].encode('UTF-8')
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
    packetPayload = {
        'message': "Hello"
    }
    packetVariableHeader = {
        'topic_name': "First",
        'packetIdentifier': b'\x00\x0a'
    }

    def parse(self):
        packet = bytearray()

        packet += packetFixedHeader['PUBLISH']

        variable_header = b'\x00'
        variable_header += bytes([len(self.packetVariableHeader['topic_name'])])
        variable_header += self.packetVariableHeader['topic_name'].encode('UTF-8')
        variable_header += self.packetVariableHeader['packetIdentifier']

        payload = b'\x00'
        payload += bytes([len(self.packetPayload['message'])])
        payload += self.packetPayload['message'].encode('UTF-8')
        variable_header += payload

        packet_length = bytes([len(variable_header)])
        packet += packet_length
        packet += variable_header

        return packet



class SUBSCRIBE(Packet):
    packetPayload = {
        'Topic_name': "Hello",
        'req_QoS': b'\x01'
    }
    packetVariableHeader = {
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
    packetVariableHeader = {
        'packetIdentifier': b'\x00\x0b'
    }
    packetPayload = {
        'Topic_name': "Hello",
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

