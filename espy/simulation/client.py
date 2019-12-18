import simpy, logging, random
from enum import Enum
from espy.simulation.packet import Packet


class State(Enum):
    SEND_PACKET = 1
    WAIT_FOR_TIMEOUT = 2
    AWAIT_ACK = 3
    FINISHED = 4


class Client(object):
    """ The client has to send one packet to a random Client. It uses a simple ARQ protocol.
		If the client gets a timeout before receiving the ack, it resends the message"""

    def __init__(self, env, id, router, num_clients):
        self.env = env
        self.id = id
        self.router = router

        self.log = logging.getLogger("Client %d" % id)
        self.state = State.SEND_PACKET

        other_clients = list(range(num_clients))
        other_clients.remove(self.id)
        self.dest = random.choice(other_clients)
        self.msg = "Hello World!"

        self.outgoing = env.process(self.process_outgoing())
        self.incoming = env.process(self.process_incoming())

    def send_packet(self, dest, msg):
        self.log.info("Send message to %d: %s", dest, msg)
        self.router.deliver_packet(Packet(self.id, dest, msg))

    def receive_packet(self, packet):
        self.log.info("Received message from %d: %s", packet.sender, packet.msg)

        if packet.msg == "ACK":
            self.state = State.FINISHED
            self.log.debug("Finished")
        else:
            self.send_packet(packet.sender, "ACK")

    def process_outgoing(self):
        while True:
            yield self.env.timeout(1)

            if self.state == State.SEND_PACKET:
                self.send_packet(self.dest, self.msg)
                self.state = State.AWAIT_ACK
            elif self.state == State.AWAIT_ACK:
                self.log.warning("Did not receive ACK. Resending...")
                self.send_packet(self.dest, self.msg)

    def process_incoming(self):
        while True:
            try:
                yield self.env.timeout(1)
            except simpy.Interrupt as e:
                self.receive_packet(e.cause)
