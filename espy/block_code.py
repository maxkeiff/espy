import numpy as np
import functools as ft


class BlockCode:

    def __init__(self, n, k):
        self._length = n
        self._dimension = k
        self._redundancy = n - k
        self._rate = k / n
        self._generator_matrix = np.zeros((k, n), dtype=int)
        self._parity_check_matrix = np.zeros((n, n - k), dtype=int)

    def __str__(self):
        return '(' + str(self._length) + ', ' + str(self._dimension) + ')' + '\n' + \
               self._generator_matrix.__str__() + '\n' + \
               self._parity_check_matrix.__str__()

    # region Properties

    @property
    def length(self):
        return self._length

    @property
    def dimension(self):
        return self._dimension

    @property
    def redundancy(self):
        return self._redundancy

    @property
    def rate(self):
        return self._rate

    @property
    def generator_matrix(self):
        return self._generator_matrix

    @property
    def parity_check_matrix(self):
        return self._parity_check_matrix

    # endregion

    def codeword_table(self):
        """
        A list of all codewords
        """
        codeword_table = np.empty([2 ** self._dimension, self._length], dtype=np.int)
        for i in range(2 ** self._dimension):
            message = np.array([(i >> j) & 1 for j in range(self._dimension)])
            codeword_table[i] = self.encode(message)
        return codeword_table

    def encode(self, message):
        """
        Encodes a message to a codeword
        """
        if len(message) != self._dimension:
            raise ValueError("length of message is unequal to k")
        codeword = np.dot(message, self._generator_matrix) % 2
        return codeword

    def decode(self, codeword):
        """
        Decodes the message from a codeword
        """
        if len(codeword) != self._length:
            raise ValueError("length of message is unequal to n")
        raise NotImplementedError

    def check(self, codeword):
        raise NotImplementedError
        # TODO check if H * codeword ^ T == 0


class NonSystematicCode(BlockCode):

    def check(self, codeword):
        pass

    def decode(self, codeword):
        if len(codeword) != self.n:
            raise ValueError("length of message is unequal to n")
        return np.dot(codeword, np.linalg.inv(self.generator_matrix)) % 2


class SystematicCode(BlockCode):

    def __init__(self, generator_matrix):
        k, n = generator_matrix.shape
        super().__init__(n, k)
        self._generator_matrix = generator_matrix
        self._information_set = np.arange(self._redundancy, self._length)
        # create parity check matrix
        sub_matrix = self._generator_matrix[:, self._length-self._dimension+1:]
        sub_matrix = sub_matrix.transpose()
        identity_matrix = np.identity(self._length-self._dimension, dtype=int)
        self._parity_check_matrix = np.hstack((sub_matrix, identity_matrix))

    def check(self, codeword):
        pass

    @property
    def information_set(self):
        return self._information_set

    def decode(self, codeword):
        if len(codeword) != self._length:
            raise ValueError("length of message is unequal to n")
        return codeword[self.information_set]
