#!/usr/bin/env python
# coding: utf-8

# In[2]:


from simulation.error_setup import ErrorSimulationSetup
from algorithms.cc_viterbi import *
from algorithms.channel_noise_simulator import channel_noise_simulator

class SimpleErrorViterbiSetup(ErrorSimulationSetup):
    def __init__(self, p, *args, **kwargs):
        """Initializes a Simulation Setup with bit flip probability p"""
        self.p = p
        self.cns = channel_noise_simulator
        super().__init__(*args, crc_size=0, **kwargs)

    def encode_message(self, msg):
        return cc_viterbi.encode_message(msg)

    def decode_message(self, msg):        
        return cc_viterbi.decode_message(msg)

    def apply_channel(self, bitstring):
        new_bitstring = cns.randomise_bits_string_list(bitstring,self.p)
        return new_bitstring

