import random

from simulation.simulator import Simulation
from simulation.error_setup import ErrorSimulationSetup
from setups.simulation_simple_error_crc import SimpleErrorCRCSetup

if __name__ == "__main__":
    random.seed(42)

    error_setup = SimpleErrorCRCSetup(p=0.001, packet_size=100)
    simulation = Simulation(error_setup)
    simulation.run(1000)
