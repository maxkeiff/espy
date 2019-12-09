import numpy
class channelNoiseSimulator:
    """Class to hold usefull funktions to simulate noise in a channel"""

    def __init__(self):
        return

    def createRandomBits (self, len):
        """create a random len bits long bitstring """

        bits = []
        for i in range (len):
            bits.append(numpy.random.randint(0, 2))

        return bits

    def randomiseBits (self, bits, probability = 0):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1]

        """

        newBits = []
        for b in bits:
            if (probability > numpy.random.random()):#roll random numbers
                newBits.append((b+1)%2)#turn 0 to 1 and 1 to 0
            else:
                newBits.append(b)

        return newBits

    def randomiseBitsBurst (self, bits, burstProbability = 0 , errorRateInBurst = 0.9 ,maxBurstLength = 8):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1], the maximum length of a burst error,the rate of errors within the bursterror[0-1]

        """

        newBits = []
        i=0
        while (i < len(bits)):
            if (burstProbability > numpy.random.random()):#roll random numbers
                curentBurstLength = 0
                burstLength = numpy.random.randint(1,high = maxBurstLength+1)

                while (burstLength > curentBurstLength and i < len(bits)):#stop on burst end,#stop when bitstream ends (simulate one bursterror and adjust i)
                    if (errorRateInBurst > numpy.random.random()):
                        newBits.append((bits[i]+1)%2)#turn 0 to 1 and 1 to 0 randomly
                    else:
                        newBits.append(bits[i])
                    curentBurstLength+=1
                    i+=1
            else:
                newBits.append(bits[i])
                i+=1


        return newBits

    def compareAndHighlightDifferences (self, bits1,bits2):
        """compare two bitlists and higlight the differences"""
        differences = []
        if (len(bits1) != len(bits2)):
            print "waning, different lengths detected. may result in higher errorrate"
        minLength = min(len(bits1),len(bits2))
        for i in range(minLength):
            differences.append(1 if bits1[i]!=bits2[i] else 0)
        print("Differences found: " + str( differences.count(True)))
        return differences


"""c=channelNoiseSimulator()
print c.randomiseBits([1,0,1,0,1,0,1,0,1,0,1,0],0.5)
print c.compareAndHighlightDifferences([1,1,1,0,0,1,1,0,0,1,0,1,1,1],[0,1,1,0,0,1,1,1,1,1,0,1,0,1])
randomBits=c.createRandomBits(200)
rb = c.randomiseBitsBurst(randomBits,0.01,.8,16)
print c.compareAndHighlightDifferences(randomBits,rb)
"""
