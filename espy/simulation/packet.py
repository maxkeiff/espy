import json


class Packet:
    """A dataclass for packets that has additional attributes for storing simulation results."""

    def __init__(
        self,
        packet_id,
        payload,
        msg,
        msg_received=None,
        payload_received=None,
        payload_valid=None,
    ):
        self.packet_id = packet_id
        self.payload = payload
        self.msg_sent = msg

        # Parameters that will be set later
        self.msg_received = msg_received
        self.payload_received = payload_received
        self.payload_valid = payload_valid

    def __repr__(self):
        return 'packet_id={}, payload="{}", payload_received="{}", payload_valid={}, msg_sent="{}", msg_received="{}"'.format(
            self.packet_id,
            self.payload,
            self.payload_received,
            self.payload_valid,
            self.msg_sent,
            self.msg_received,
        )

    def to_dict(self):
        json_dict = {
            "packet_id": self.packet_id,
            "payload": self.payload,
            "payload_received": self.payload_received,
            "payload_valid": self.payload_valid,
            "msg_sent": self.msg_sent,
            "msg_received": self.msg_received,
        }
        return json_dict


class ARQPacket:
    def __init__(self, packet_id):
        self.packet_id = packet_id
