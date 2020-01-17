import simpy, logging, random
import time
from collections import deque
from simulation.packet import Packet


class Sender:
    """ The client has to send one packet to a random Client. It uses a (simple ARQ protocol."""

    def __init__(self, env, channel, error_setup):
        self.env = env
        self.channel = channel
        self.error_setup = error_setup

        self.payload_len = error_setup.payload_size
        self.resend_queue = deque([])
        self.message_generator = self.next_message()

        self.log = logging.getLogger("Sender")
        self.package_log = []

        self.outgoing = env.process(self.process_outgoing())

    def get_packets(self):
        return self.package_log

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

    def send_packet(self, packet_id):
        self.log.info("Send message {}.".format(packet_id))

        payload = "{0:b}".format(random.getrandbits(self.payload_len)).zfill(
            self.payload_len
        )
        payload_with_crc = self.error_setup.crc_add(payload)
        payload_with_crc_fec = self.error_setup.fec_encode(payload_with_crc)

        packet = Packet(packet_id=packet_id, payload=payload, msg=payload_with_crc_fec)
        self.package_log.append(packet)

        self.channel.deliver_packet(packet)

    def receive_arq(self, arq_packet):
        self.log.info("Received ARQ request on packet {}.".format(arq_packet.packet_id))
        self.resend_message(arq_packet.packet_id)

    def process_outgoing(self):
        while True:
            yield self.env.timeout(1)
            time.sleep(1 / 100.0)
            packet_id = next(self.message_generator)
            self.send_packet(packet_id)
