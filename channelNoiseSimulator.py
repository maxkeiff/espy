import numpy
class channelNoiseSimulator:
    """Class to hold usefull funktions to simulate noise in a channel"""

    def __init__(self):
        return

    def createRandomBits (self, len):
        """create a random len bits long bitstring """

        bits = numpy.random.randint(2, size=(len,))

        return bits

    def randomiseBits (self, bits, probability = 0):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability [0-1]

        """

        newBits = []
        for b in bits:
            if (probability > numpy.random.random()):#roll random numbers
                newBits.append((b+1)%2)#turn 0 to 1 and 1 to 0
            else:
                newBits.append(b)

        return newBits
        
#c=channelNoiseSimulator()
#print c.randomiseBits([1,0,1,0,1,0,1,0,1,0,1,0],0.5)
