class Packet:
    """A dataclass for packets that has additional attributes for storing simulation results."""

    def __init__(self, packet_id, payload, msg):
        self.packet_id = packet_id
        self.payload = payload
        self.msg_sent = msg

        # Parameters that will be added later
        self.msg_received = None
        self.payload_received = None
        self.payload_valid = None

    def __repr__(self):
        return 'packet_id={}, payload="{}", payload_received="{}", payload_valid={}, msg_sent="{}", msg_received="{}"'.format(
            self.packet_id,
            self.payload,
            self.payload_received,
            self.payload_valid,
            self.msg_sent,
            self.msg_received,
        )


class ARQPacket:
    def __init__(self, packet_id):
        self.packet_id = packet_id
