import random
import logging

from simulation.simulator import Simulation
from simulation.error_setup import ErrorSimulationSetup
from setups.simulation_simple_error_crc import SimpleErrorCRCSetup
import evaluation.charts as charts
import evaluation.utils as utils


SIM_STEPS = 500

LOG_LEVEL = logging.WARNING


def sim_1():
    simulation_results = {}
    for i in range(200):
        p = i / (1000.0)
        error_setup = SimpleErrorCRCSetup(p=p, packet_size=20)
        simulation = Simulation(error_setup)
        simulation_results[p] = simulation.run(SIM_STEPS)

    analysed_simulation_results = utils.analyse_simulation_results(simulation_results)
    charts.ber_to_abs(analysed_simulation_results, "bit flip probability")


def sim_2(
    x_steps, xmin, xmax, y_steps, ymin, ymax, evaluate_function, y_measurement_function
):
    log = logging.Logger("Simulation")
    simulation_results = []
    for _y in range(0, y_steps):
        y = ymin + _y / y_steps * (ymax - ymin)
        simulation_results_list = []
        for _x in range(0, x_steps):
            x = xmin + _x / x_steps * (xmax - xmin)
            simulation_results_list.append(evaluate_function(x, y))
            log.warning(
                "{:.1%} finished".format((_y * x_steps + _x) / (x_steps * y_steps))
            )
        simulation_results.append(simulation_results_list)

    analysed_simulation_results = utils.analyse_3d_simulation_results(
        simulation_results, y_measurement_function
    )
    charts.two_dimension_heatmap(analysed_simulation_results, xmin, xmax, ymin, ymax)


def evaluate_ber_packet_size(packet_size, probability):
    error_setup = SimpleErrorCRCSetup(p=probability, packet_size=int(packet_size))
    simulation = Simulation(error_setup)
    return simulation.run(SIM_STEPS)


if __name__ == "__main__":
    random.seed(24)

    logging.basicConfig(
        format="[%(levelname)-7s] %(name)8s: %(message)s", level=LOG_LEVEL
    )

    sim_2(
        20,
        100,
        2000,
        100,
        0,
        0.01,
        evaluate_function=evaluate_ber_packet_size,
        y_measurement_function=utils.count_positives,
    )
