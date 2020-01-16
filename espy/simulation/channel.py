import logging, random
from packet import Packet


class Channel:
    """	Delivers packets from one sender to receiver and can sand ARQ request back to the sender. 
    Uses some channelmodel to randomly corrupt packages."""

    def __init__(self, env, apply_channel=None):
        self.env = env

        if apply_channel:
            self.apply_channel = apply_channel

        self.log = logging.getLogger("Channel")
        self.sender = None
        self.receiver = None

    def apply_channel(self, msg):
        return msg

    def deliver_packet(self, packet):
        packet.msg_received = self.apply_channel(packet.msg_sent)
        
        self.receiver.receive_packet(packet)        

    def deliver_arq_request(self, arq_packet):
        """Assume that arq requests are always received"""
        self.sender.receive_arq(arq_packet)