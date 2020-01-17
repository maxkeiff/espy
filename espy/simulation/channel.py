import logging, random
from simulation.packet import Packet


class Channel:
    """	Delivers packets from one sender to receiver and can sand ARQ request back to the sender. 
    Uses some channelmodel to randomly corrupt packages."""

    def __init__(self, env, error_setup):
        self.env = env

        self.error_setup = error_setup

        self.log = logging.getLogger("Channel")
        self.sender = None
        self.receiver = None

    def deliver_packet(self, packet):
        packet.msg_received = self.error_setup.apply_channel(packet.msg_sent)

        self.receiver.receive_packet(packet)

    def deliver_arq_request(self, arq_packet):
        """Assume that arq requests are always received"""
        self.sender.receive_arq(arq_packet)
