import random

from simulation.simulator import Simulation
from simulation.error_setup import ErrorSimulationSetup
from setups.simulation_simple_error_crc import SimpleErrorCRCSetup
import evaluation.charts as charts
import evaluation.utils as utils

if __name__ == "__main__":
    random.seed(24)

    simulation_results = {}
    for i in range(200):
        p = i / (1000.0)
        error_setup = SimpleErrorCRCSetup(p=p, packet_size=20)
        simulation = Simulation(error_setup)
        simulation_results[p] = simulation.run(1000)
    
    analyzes_simulation_results = utils.analyse_simulation_results(simulation_results)
    charts.ber_to_abs(analyzes_simulation_results, "bit flip probability")



