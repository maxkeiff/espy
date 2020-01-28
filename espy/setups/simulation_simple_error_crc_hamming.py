from simulation.error_setup import ErrorSimulationSetup
from algorithms.channel_noise_simulator import channel_noise_simulator
from algorithms.crc import CRC_8

class CRCHammingErrorSetup(ErrorSimulationSetup):
    def __init__(self, p, rate = 0.5, *args, **kwargs):
        """Initializes a Simulation Setup with bit flip probability p"""
        self.p = p
        self.cns = channel_noise_simulator()
        self.rate = rate
        self.crc = CRC_8()
        fec_size = 0 # TODO
        super().__init__(*args, crc_size=8, fec_size=fec_size, **kwargs)

    def apply_channel(self, bitstring):
        new_bitstring = self.cns.randomise_bits_string_list(bits=bitstring, probability=self.p)
        new_bitstring = "".join(new_bitstring)
        return new_bitstring

    def crc_add(self, msg):
        return self.crc.crc_encode(msg)

    def crc_check_and_remove(self, msg):
        return self.crc.crc_decode(msg)

    def fec_encode(self, msg):
        raise NotImplementedError

    def fec_decode(self, msg):
        raise NotImplementedError
