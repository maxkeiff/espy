import simpy, logging

from simulation.sender import Sender
from simulation.receiver import Receiver
from simulation.channel import Channel


class Simulation:
    def __init__(self, error_setup):
        self.env = simpy.Environment()
        self.error_setup = error_setup
        self.channel = Channel(self.env, self.error_setup)
        self.sender = Sender(self.env, self.channel, self.error_setup)
        self.receiver = Receiver(self.env, self.channel, self.error_setup)

        self.channel.sender = self.sender
        self.channel.receiver = self.receiver

    def run(self, duration):
        logging.info("Simulation starting")
        self.env.run(until=duration)
        logging.info("Simulation finished")

        return self.sender.get_packets()
