class ErrorSimulationSetup:
    def __init__(self, packet_size, crc_size=0, fec_size=0):
        self.packet_size = packet_size

        self.crc_size = crc_size
        self.fec_size = fec_size
        self.payload_size = self.packet_size - (self.crc_size + self.fec_size)

    def fec_encode(self, msg):
        return msg

    def fec_decode(self, msg):
        return msg

    def crc_add(self, msg):
        return msg

    def crc_check_and_remove(self, msg):
        return msg, True

    def apply_channel(self, bitstring):
        return bitstring
