import numpy
class channelNoiseSimulator:
    """Class to hold usefull funktions to simulate noise in a channel"""

    def __init__(self):
        return

    def createRandomBits (self, len):
        """create a random len bits long bitstring """

        bits = numpy.random.randint(2, size=(len,))

        return bits
