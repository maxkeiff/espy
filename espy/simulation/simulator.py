import simpy, logging
from sender import Sender, ErrorSetup, Receiver
from channel import Channel

SIM_TOTAL_DURATION = 1000
LOG_LEVEL = logging.INFO

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)-7s] %(name)8s: %(message)s', level=LOG_LEVEL)

    # init simpy and network
    env = simpy.Environment()
    channel = Channel(env)
    error_setup = ErrorSetup()
    sender = Sender(env, channel, error_setup, 10)
    receiver = Receiver(env, channel, error_setup)
    channel.sender = sender
    channel.receiver = receiver

    logging.info("Simulation starting")
    env.run(until=SIM_TOTAL_DURATION)
    logging.info("Simulation finished")

    for packet in sender.get_packets():
        print(packet)