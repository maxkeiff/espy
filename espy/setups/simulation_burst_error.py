from simulation.error_setup import ErrorSimulationSetup
from algorithms.channel_noise_simulator import channel_noise_simulator
import random


class SimpleErrorCRCSetup(ErrorSimulationSetup):
    def __init__(self, p_enter,p_leave, *args, **kwargs):
        """Initializes a Simulation Setup with only Bursterrors and probability p_enter to start bursting
         and probability p_leave to stop bursting"""


        self.cns = channel_noise_simulator()
        self.p_enter = p_enter
        self.p_leave = p_leave
        super().__init__(*args, crc_size=self.crc.n, **kwargs)


    def apply_channel(self, bitstring):
        return self.cns.randomise_bits_burst_string(bitstring,self.p_enter,self.p_leave)
