from abc import ABC, abstractmethod

packetFixedHeader = {
    'CONNECT': b'\x10',
    'PUBLISH': b'\x30',
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

class PUBLISH(Packet):
    pass

class SUBSCRIBE(Packet):
    pass

class UNSUBSCRIBE(Packet):
    pass

class PINGREQ(Packet):
    pass