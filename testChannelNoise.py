from channelNoiseSimulator import channelNoiseSimulator
import numpy

numpy.random.seed(42)


def test_bitGen():
    cns = channelNoiseSimulator()
    res=numpy.alltrue(cns.createRandomBits(10) == [0,1,0,0,0,1,0,0,0,1])
    assert res
def test_simpleRandom():
    cns = channelNoiseSimulator()
    res=numpy.alltrue(cns.randomiseBits( [0,1,0,1,0,1,0,1,0,1],0.5)==[1, 0, 0, 1, 0, 0, 0, 1, 1, 0])
    assert res
#test_bitGen()
#test_simpleRandom()


#cns = channelNoiseSimulator()
