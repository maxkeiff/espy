import simpy, logging, random
from collections import deque
from simulation.packet import ARQPacket


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
