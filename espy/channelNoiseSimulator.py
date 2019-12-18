import numpy
class channel_noise_simulator:
    """Class to hold usefull funktions to simulate noise in a channel"""

    def __init__(self):
        return
    #_____________create bits___________________
    def create_random_bits_list (self, len):
        """create a random len bits long bitstring """

        bits = []
        for i in range (len):
            bits.append(numpy.random.randint(0, 2))

        return bits

    def create_random_bits_string (self, len):
        """create a random len bits long string """

        bits = ""
        for i in range (len):
            bits+= str(numpy.random.randint(0, 2))

        return bits
    #_____________Randoise bits______________________
    def randomise_bits_list (self, bits, probability ):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1]
            RETURN: a list of bits
        """

        new_bits = []
        for b in bits:
            if (probability > numpy.random.random()):#roll random numbers
                new_bits.append((b+1)%2)#turn 0 to 1 and 1 to 0
            else:
                new_bits.append(b)

        return new_bits

    def randomise_bits_string (self, bits, probability ):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1]
            Return: a string full of bits
        """

        new_bits = ""
        for b in bits:
            if (probability > numpy.random.random()):#roll random numbers
                new_bits+=str((int(b)+1)%2)#turn 0 to 1 and 1 to 0
            else:
                new_bits+=b

        return new_bits

    def randomise_bits_burst_list (self, bits, burst_probability  , error_rate_in_burst = 0.9 ,max_burst_length = 8):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1], the maximum length of a burst error,the rate of errors within the bursterror[0-1]
            Return: list of bits with added burst erorrs
        """

        new_bits = []
        i=0
        while (i < len(bits)):
            if (burst_probability > numpy.random.random()):#roll random numbers
                curent_burst_length = 0
                burst_length = numpy.random.randint(1,high = max_burst_length+1)

                while (burst_length > curent_burst_length and i < len(bits)):#stop on burst end,#stop when bitstream ends (simulate one bursterror and adjust i)
                    if (error_rate-in_burst > numpy.random.random()):
                        new_bits.append((bits[i]+1)%2)#turn 0 to 1 and 1 to 0 randomly
                    else:
                        new_bits.append(bits[i])
                    curent_burst_length+=1
                    i+=1
            else:
                new_bits.append(bits[i])
                i+=1


        return new_bits

    def randomise_bits_burst_string (self, bits, burst_probability  , error_rate_in_burst = 0.9 ,max_burst_length = 8):
        """A function to simply flip bits with the given probability
            ARGS: a list of bits, the probability for an error[0-1], the maximum length of a burst error,the rate of errors within the bursterror[0-1]
            Return: String of bits with added burst erorrs
        """

        new_bits = ""
        i=0
        while (i < len(bits)):
            if (burst_probability > numpy.random.random()):#roll random numbers
                curent_burst_length = 0
                burst_length = numpy.random.randint(1,high = max_burst_length+1)

                while (burst_length > curent_burst_length and i < len(bits)):#stop on burst end,#stop when bitstream ends (simulate one bursterror and adjust i)
                    if (error_rate_in_burst > numpy.random.random()):
                        new_bits+=str(((int(bits[i])+1)%2))#turn 0 to 1 and 1 to 0 randomly
                    else:
                        new_bits+=str(bits[i])
                    curent_burst_length+=1
                    i+=1
            else:
                new_bits+=str(bits[i])
                i+=1


        return new_bits
    #______________compare bits__________________________
    def compare_and_highlight_differences (self, bits1,bits2):
        """compare two bitlists and higlight the differences"""
        differences = []
        if (len(bits1) != len(bits2)):
            print("waning, different lengths detected. may result in higher errorrate")
        min_length = min(len(bits1),len(bits2))
        for i in range(min_length):
            differences.append(1 if bits1[i]!=bits2[i] else 0)
        print("Differences found: " + str( differences.count(True)))
        return differences




#c=channel_noise_simulator()
#print c.randomise_bits_list([1,1,1,1,0,0,0,0,1],0.5)
#print c.randomise_bits_string("1101110",0.5)
#print c.compare_and_highlight_differences([1,1,1,0,0,1,1,0,0,1,0,1,1,1],[0,1,1,0,0,1,1,1,1,1,0,1,0,1])
#print c.create_random_bits_list(200)
#rb= c.create_random_bits_string(200)
#rr = c.randomise_bits_burst_string(rb,0.01,.8,16)

#print c.compare_and_highlight_differences("11110000","11001100")
#"""
