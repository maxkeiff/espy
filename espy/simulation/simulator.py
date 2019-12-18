import simpy, logging
from espy.simulation.client import Client
from espy.simulation.router import Router

NUM_CLIENTS = 3
SIM_TOTAL_DURATION = 1000
ROUTER_DROP_PROB = 0.3
SPEED = 0.2
LOG_LEVEL = logging.INFO

def init_clients():
    clients = []
    for i in range(NUM_CLIENTS):
        clients.append(Client(env, i, router, NUM_CLIENTS))
    return clients

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)-7s] %(name)8s: %(message)s', level=LOG_LEVEL)

    # init simpy and network
    env = simpy.Environment()
    router = Router(env, ROUTER_DROP_PROB, SPEED)
    clients = init_clients()
    router.store_clients(clients)

    logging.info("Simulation starting")
    env.run(until=SIM_TOTAL_DURATION)
    logging.info("Simulation finished")