from simulation.error_setup import ErrorSimulationSetup
from algorithms.crc import CRC_8
import random


class SimpleErrorCRCSetup(ErrorSimulationSetup):
    def __init__(self, p, *args, **kwargs):
        """Initializes a Simulation Setup with CRC8 and bit flip probability p"""

        self.crc = CRC_8()
        self.p = p
        super().__init__(*args, crc_size=self.crc.n, **kwargs)

    def crc_add(self, msg):
        return self.crc.crc_encode(msg)

    def crc_check_and_remove(self, msg):
        return self.crc.crc_decode(msg)

    def apply_channel(self, bitstring):
        reverse = {"1": "0", "0": "1"}

        new_bitstring = "".join(
            [c if random.random() > self.p else reverse.get(c) for c in bitstring]
        )
        return new_bitstring
