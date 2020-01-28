import random
import logging
import json

from simulation.simulator import Simulation
from simulation.error_setup import ErrorSimulationSetup
from setups.simulation_simple_error_crc import SimpleErrorCRCSetup
from setups.simulation_simple_error_viterbi import SimpleErrorViterbiSetup

from setups.simulation_burst_error_crc import BurstErrorCRCSetup
from setups.simulation_burst_error import BurstErrorSetup
import evaluation.charts as charts
import evaluation.utils as utils


SIM_STEPS = 100

LOG_LEVEL = logging.WARNING


def sim_1(file=None):
    simulation_results = {}
    if not file:
        for i in range(200):
            p = i / (1000.0)
            # error_setup = SimpleErrorCRCSetup(p=p, packet_size=20)
            error_setup = SimpleErrorViterbiSetup(p=p, rate=0.25, packet_size=100)
            simulation = Simulation(error_setup)
            simulation_results[p] = utils.analyse_packet_list(simulation.run(SIM_STEPS))

        with open("sim_1.json", "w+") as json_file:
            json_file.write(json.dumps(simulation_results))
    else:
        with open(file, "w+") as json_file:
            simulation_results = json.loads(json_file.read())

    charts.ber_to_abs(simulation_results, "bit flip probability")


def sim_2(
    x_steps, xmin, xmax, y_steps, ymin, ymax, evaluate_function, keyword, file=None
):
    log = logging.Logger("Simulation")
    simulation_results = []

    if not file:
        for _y in range(0, y_steps):
            y = ymin + _y / y_steps * (ymax - ymin)
            simulation_results_list = []
            for _x in range(0, x_steps):
                x = xmin + _x / x_steps * (xmax - xmin)
                simulation_results_list.append(
                    utils.analyse_packet_list(evaluate_function(x, y))
                )
                log.warning(
                    "{:.1%} finished".format((_y * x_steps + _x) / (x_steps * y_steps))
                )
            simulation_results.append(simulation_results_list)

        with open("sim_2.json", "w+") as json_file:
            json_file.write(json.dumps(simulation_results))
    else:
        with open(file, "r+") as json_file:
            simulation_results = json.loads(json_file.read())

    analysed_simulation_results = utils.analyse_3d_simulation_results(
        simulation_results, keyword
    )
    charts.two_dimension_heatmap(analysed_simulation_results, xmin, xmax, ymin, ymax)

def sim_3(file=None):#crc and burst
    simulation_results = {}
    if not file:
        for i in range(200):
            error_density_multiplyer = i/10
            error_setup = BurstErrorCRCSetup(p_enter=(0.001*error_density_multiplyer),p_leave=(1-(0.01*error_density_multiplyer)),packet_size=20 )
            simulation = Simulation(error_setup)
            simulation_results[(0.001*error_density_multiplyer)] = utils.analyse_packet_list(simulation.run(SIM_STEPS))

        with open("sim_1.json", "w+") as json_file:
            json_file.write(json.dumps(simulation_results))
    else:
        with open(file, "w+") as json_file:
            simulation_results = json.loads(json_file.read())

    charts.ber_to_abs(simulation_results, "Burst start probability")

def sim_4(file=None):#burst only
    simulation_results = {}
    if not file:
        for i in range(200):
            error_density_multiplyer = i/10
            error_setup = BurstErrorSetup(p_enter=(0.001*error_density_multiplyer),p_leave=(1-(0.01*error_density_multiplyer)),packet_size=20 )
            simulation = Simulation(error_setup)
            simulation_results[(0.001*error_density_multiplyer)] = utils.analyse_packet_list(simulation.run(SIM_STEPS))

        with open("sim_1.json", "w+") as json_file:
            json_file.write(json.dumps(simulation_results))
    else:
        with open(file, "w+") as json_file:
            simulation_results = json.loads(json_file.read())

    charts.ber_to_abs(simulation_results, "Burst start probability")



def evaluate_ber_packet_size(packet_size, probability):
    error_setup = SimpleErrorCRCSetup(p=probability, packet_size=int(packet_size))
    simulation = Simulation(error_setup)
    return simulation.run(SIM_STEPS)


if __name__ == "__main__":
    random.seed(24)

    logging.basicConfig(
        format="[%(levelname)-7s] %(name)8s: %(message)s", level=LOG_LEVEL
    )

    '''sim_2(
        20,
        100,
        2000,
        100,
        0,
        0.01,
        evaluate_function=evaluate_ber_packet_size,
        keyword="positives",
    )'''
    # sim_3()
    sim_1()
