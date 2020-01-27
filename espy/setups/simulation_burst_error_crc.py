from simulation.error_setup import ErrorSimulationSetup
from algorithms.crc import CRC_8
from algorithms.channel_noise_simulator import channel_noise_simulator


class BurstErrorCRCSetup(ErrorSimulationSetup):
    def __init__(self, p_enter,p_leave, *args, **kwargs):
        """Initializes a Simulation Setup with only Bursterrors and probability p_enter to start bursting
         and probability p_leave to stop bursting and with CRC8"""

        self.crc = CRC_8()

        self.cns = channel_noise_simulator()
        self.p_enter = p_enter
        self.p_leave = p_leave
        super().__init__(*args, **kwargs)

    def crc_add(self, msg):
        return self.crc.crc_encode(msg)

    def crc_check_and_remove(self, msg):
        return self.crc.crc_decode(msg)

    def apply_channel(self, bitstring):
        return self.cns.randomise_bits_burst_string(bitstring,self.p_enter,self.p_leave)
