from channelNoiseSimulator import channelNoiseSimulator
import numpy

numpy.random.seed(42)


def test_bitGen():
    cns = channelNoiseSimulator()
    numpy.alltrue(cns.createRandomBits(10) == [0,1,0,0,0,1,0,0,0,1])

test_bitGen()
#cns = channelNoiseSimulator()
#print( cns.createRandomBits(10))
