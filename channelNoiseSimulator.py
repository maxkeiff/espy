import numpy
class channelNoiseSimulator:
    """Class to hold usefull funktions to simulate noise in a channel"""

    def __init__(self):
        return
    #_____________create bits___________________
    def createRandomBitsList (self, len):
        """create a random len bits long bitstring """

        bits = []
        for i in range (len):
            bits.append(numpy.random.randint(0, 2))

        return bits

    def createRandomBitsString (self, len):
        """create a random len bits long string """

        bits = ""
        for i in range (len):
            bits+= str(numpy.random.randint(0, 2))

        return bits
    #_____________Randoise bits______________________
    def randomiseBitsList (self, bits, probability ):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1]
            RETURN: a list of bits
        """

        newBits = []
        for b in bits:
            if (probability > numpy.random.random()):#roll random numbers
                newBits.append((b+1)%2)#turn 0 to 1 and 1 to 0
            else:
                newBits.append(b)

        return newBits

    def randomiseBitsString (self, bits, probability ):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1]
            Return: a string full of bits
        """

        newBits = ""
        for b in bits:
            if (probability > numpy.random.random()):#roll random numbers
                newBits+=str((int(b)+1)%2)#turn 0 to 1 and 1 to 0
            else:
                newBits+=b

        return newBits

    def randomiseBitsBurstList (self, bits, burstProbability  , errorRateInBurst = 0.9 ,maxBurstLength = 8):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1], the maximum length of a burst error,the rate of errors within the bursterror[0-1]
            Return: list of bits with added burst erorrs
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

    def randomiseBitsBurstString (self, bits, burstProbability  , errorRateInBurst = 0.9 ,maxBurstLength = 8):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1], the maximum length of a burst error,the rate of errors within the bursterror[0-1]
            Return: String of bits with added burst erorrs
        """

        newBits = ""
        i=0
        while (i < len(bits)):
            if (burstProbability > numpy.random.random()):#roll random numbers
                curentBurstLength = 0
                burstLength = numpy.random.randint(1,high = maxBurstLength+1)

                while (burstLength > curentBurstLength and i < len(bits)):#stop on burst end,#stop when bitstream ends (simulate one bursterror and adjust i)
                    if (errorRateInBurst > numpy.random.random()):
                        newBits+=str(((int(bits[i])+1)%2))#turn 0 to 1 and 1 to 0 randomly
                    else:
                        newBits+=str(bits[i])
                    curentBurstLength+=1
                    i+=1
            else:
                newBits+=str(bits[i])
                i+=1


        return newBits
    #______________compare bits__________________________
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




c=channelNoiseSimulator()
#print c.randomiseBitsList([1,1,1,1,0,0,0,0,1],0.5)
#print c.randomiseBitsString("1101110",0.5)
#print c.compareAndHighlightDifferences([1,1,1,0,0,1,1,0,0,1,0,1,1,1],[0,1,1,0,0,1,1,1,1,1,0,1,0,1])
#print c.createRandomBitsList(200)
#rb= c.createRandomBitsString(200)
#rr = c.randomiseBitsBurstString(rb,0.01,.8,16)

print c.compareAndHighlightDifferences("11110000","11001100")
#"""
