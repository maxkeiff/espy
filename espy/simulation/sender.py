import simpy, logging, random
from collections import deque
from enum import Enum
from packet import Packet, ARQPacket


class State(Enum):
    SEND_PACKET = 1
    WAIT_FOR_TIMEOUT = 2
    AWAIT_ACK = 3
    FINISHED = 4

class MessageQueue:

    def __init__(self):
        self.resend_queue = deque([])

    def resend_message(self, msg_number: int):
        self.resend_queue.append(msg_number)

    def next_message(self):
        current_message = 0
        while True:
            if len(self.resend_queue) > 0:
                yield self.resend_queue.popleft()
            else:
                yield current_message
                current_message += 1

class ErrorSetup:

    def __init__(self):
        self.crc_size = 0
        self.fec_size = 0

    def fec_encode(self, msg):
        return msg

    def fec_decode(self, msg):
        return msg

    def crc_add(self, msg):
        return msg

    def crc_check_and_remove(self, msg):
        return msg, True


class Sender:
    """ The client has to send one packet to a random Client. It uses a (simple ARQ protocol."""

    def __init__(self, env, channel, error_setup, message_len):
        self.env = env
        self.channel = channel 
        self.error_setup = error_setup

        self.payload_len =  message_len - (error_setup.crc_size + error_setup.fec_size)
        self.send_buffer = MessageQueue()
        self.message_generator = self.send_buffer.next_message()

        self.log = logging.getLogger("Sender")
        self.package_log = []

        self.outgoing = env.process(self.process_outgoing())

    def get_packets(self):
        return self.package_log

    def send_packet(self, packet_id):
        self.log.info("Send message {}.".format(packet_id))

        random.seed(packet_id)
        payload = random.getrandbits(self.payload_len)
        payload_with_crc = self.error_setup.crc_add(payload)
        payload_with_crc_fec = self.error_setup.fec_encode(payload_with_crc)

        packet = Packet(packet_id=packet_id, payload=payload, msg=payload_with_crc_fec)
        self.package_log.append(packet)

        self.channel.deliver_packet(packet)

    def receive_arq(self, arq_packet):
        self.log.info("Received ARQ request on packet {}.".format(arq_packet.packet_id))
        self.send_buffer.resend_message(arq_packet.packet_id)

    def process_outgoing(self):
        while True:
            yield self.env.timeout(1)
            packet_id = next(self.message_generator)
            self.send_packet(packet_id)


class Receiver:

    def __init__(self, env, channel, error_setup):
        self.env = env
        self.channel = channel
        self.error_setup = error_setup

        self.log = logging.getLogger("Receiver")

        self.arq_queue = deque([])
        self.outgoing = env.process(self.process_outgoing())

    def send_arq(self, packet_id):
        self.log.info("Send ARQ request for {}.".format(packet_id))

        packet = ARQPacket(packet_id)
        self.channel.deliver_arq_request(packet)

    def receive_packet(self, packet):
        self.log.info("Message for packet {}.".format(packet.packet_id))

        msg_with_crc_fec = packet.msg_received
        msg_with_crc = self.error_setup.fec_decode(msg_with_crc_fec)
        msg, crc_valid = self.error_setup.crc_check_and_remove(msg_with_crc)

        # Evaluate package
        packet.payload_received = msg
        packet.payload_valid = crc_valid
        
        if not crc_valid:
            self.arq_queue.append(packet.packet_id)

    def process_outgoing(self):
        while True:
            yield self.env.timeout(1)
            if len(self.arq_queue) > 0:
                packet_id = self.arq_queue.popleft()
                self.send_arq(packet_id)
