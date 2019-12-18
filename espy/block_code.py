import numpy as np
import functools as ft


class BlockCode:

    def __init__(self, n, k):
        self._length = n
        self._dimension = k

    @property
    def length(self):
        return self._length

    @property
    def dimension(self):
        return self._dimension

    @property
    @ft.lru_cache()
    def redundancy(self):
        return self._length - self._dimension

    @property
    @ft.lru_cache()
    def information_set(self):
        return np.arange(self.redundancy, self._length)

    @property
    @ft.lru_cache()
    def rate(self):
        return self._dimension / self._length

    @property
    @ft.lru_cache()
    def minimum_distance(self):
        # TODO min hamming distance
        raise NotImplementedError
        return 0

    @property
    def generator_matrix(self):
        return self.generator

    @property
    def parity_check_matrix(self):
        return self.parity_check

    @property
    def codeword_table(self):
        """
        A list of all codewords
        """
        codeword_table = np.empty([2**self._dimension, self._length], dtype=np.int)
        for i in range(2**self._dimension):
            message = np.array([(i >> j) & 1 for j in range(self._dimension)])
            codeword_table[i] = self.encode(message)
        return self.codeword_table

    def create_generator(self):
        """
        p is the length of the payload
        n is the length of the block
        """
        # TODO generate matrix
        
        # self.generator = 
        # self.parity_check = 
        raise NotImplementedError

    def encode(self, message):
        """
        Encodes a message to a codeword
        """
        if len(message) != self._dimension:
            raise ValueError("length of message is unequal to k")
        codeword = np.dot(message, self.generator_matrix) % 2
        return codeword

    def decode(self, codeword):
        """
        Decodes the message from a codeword
        """
        if len(codeword) != self._length:
            raise ValueError("length of message is unequal to n")
        return message

    def checkCodeword(self, codeword):
        raise NotImplementedError
        # TODO
        # check if H * codeword ^ T == 0
        return 1


class NonSystematicCode(BlockCode):

    def createGenerator(self, p , n):
        return super().createGenerator()

    def decode(self, codeword):
        if len(codeword) != self.n:
            raise ValueError("length of message is unequal to n")
        return np.dot(codeword, numpy.linalg.inv(self.generator_matrix)) % 2


class SystematicCode(BlockCode):

    def createGenerator(self, p, n):
        return super().createGenerator()

    def decode(self, codeword):
        if len(codeword) != self.n:
            raise ValueError("length of message is unequal to n")
        return codeword[self.information_set]