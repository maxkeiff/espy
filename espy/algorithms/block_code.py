import itertools
import numpy as np


# region utility

def hamming(x, y):
    return list(map(lambda z: z[0] ^ z[1], list(zip(x, y)))).count(1)


# endregion


class BlockCode:

    def __init__(self, n, k):
        self._length = n
        self._dimension = k
        self._redundancy = n - k
        self._rate = k / n
        self._generator_matrix = np.zeros((k, n), dtype=int)
        self._parity_check_matrix = np.zeros((n, n - k), dtype=int)
        self._hamming_distance = 0

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

    @property
    def hamming_distance(self):
        return self._hamming_distance

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

    def validate(self, codeword):
        """
        Validates whether a codeword belongs to this block code or not
        """
        codeword = np.array(codeword)
        codeword_t = codeword.transpose()
        res = np.dot(self._parity_check_matrix, codeword_t) % 2
        return not res.any()

    def maximum_likelihood_decode(self, codeword):
        """
        Selects the message with the smallest hamming distance to the decoded codeword
        """
        codeword_array = np.array(codeword)
        all_codes = list()
        all_codes.append(codeword_array)
        for i in range(len(codeword_array)):
            codes = [codeword_array]
            for j in range(i + 1):
                new_codes = []
                for code in codes:
                    for k in range(len(code)):
                        x = code.copy()
                        x[k] = 1 - x[k]
                        x_not_in_all_codes = len(list(filter(lambda y: np.array_equal(x, y), all_codes))) == 0
                        x_not_in_new_codes = len(list(filter(lambda y: np.array_equal(x, y), new_codes))) == 0
                        if j < i or x_not_in_all_codes:
                            if x_not_in_new_codes:
                                new_codes.append(x)
                            if x_not_in_all_codes:
                                all_codes.append(x)
                codes = new_codes.copy()
            # print("dist", i + 1, "len", len(codes), codes)
            for code in codes:
                if self.validate(code):
                    # print(code, self._parity_check_matrix.dot(np.transpose(code)))
                    return code


class NonSystematicCode(BlockCode):

    def __init__(self, generator_matrix):
        k, n = generator_matrix.shape
        super().__init__(n, k)
        self._generator_matrix = generator_matrix
        # create parity check matrix
        # TODO calculate parity check matrix
        # calculate hamming distance
        word_combos = list(itertools.combinations(self.codeword_table(), 2))
        self._hamming_distance = min(list(map(lambda x: hamming(x[0], x[1]), word_combos)))

    def decode(self, codeword):
        if len(codeword) != self.n:
            raise ValueError("length of message is unequal to n")
        return np.dot(codeword, self.parity_check_matrix) % 2


class SystematicCode(BlockCode):

    def __init__(self, generator_matrix):
        k, n = generator_matrix.shape
        super().__init__(n, k)
        self._generator_matrix = generator_matrix
        self._information_set = np.arange(self._redundancy, self._length)
        # create parity check matrix
        sub_matrix = self._generator_matrix[:, self._length - self._dimension + 1:]
        sub_matrix = sub_matrix.transpose()
        identity_matrix = np.identity(self._length - self._dimension, dtype=int)
        self._parity_check_matrix = np.hstack((sub_matrix, identity_matrix))
        # calculate hamming distance
        word_combos = list(itertools.combinations(self.codeword_table(), 2))
        self._hamming_distance = min(list(map(lambda x: hamming(x[0], x[1]), word_combos)))

    @property
    def information_set(self):
        return self._information_set

    def decode(self, codeword):
        if len(codeword) != self._length:
            raise ValueError("length of message is unequal to n")
        return codeword[self.information_set]


class HammingCode(BlockCode):

    def __init__(self, redundancy, extended=False, information_set='left'):
        # default init of super class
        super().__init__(1, 1)

        # create parity check sub matrix
        parity_sub_matrix = np.zeros((2 ** redundancy - redundancy - 1, redundancy), dtype=np.int)
        i = 0
        for w in range(2, redundancy + 1):
            for idx in itertools.combinations(range(redundancy), w):
                parity_sub_matrix[i, list(idx)] = 1
                i += 1
        self.extended = extended
        if extended:
            last_column = (1 + np.sum(parity_sub_matrix, axis=1)) % 2
            extended_parity_sub_matrix = np.hstack([parity_sub_matrix, last_column[np.newaxis].T])
            parity_sub_matrix = extended_parity_sub_matrix

        ####

        self._parity_sub_matrix = np.array(parity_sub_matrix, dtype=np.int) % 2
        self._dimension, self._redundancy = self._parity_sub_matrix.shape
        self._length = self._dimension + self._redundancy
        #
        if information_set == 'left':
            information_set = np.arange(self._dimension)
        elif information_set == 'right':
            information_set = np.arange(self._redundancy, self._length)
        self._information_set = np.array(information_set, dtype=np.int)
        if self._information_set.size != self._dimension or \
                self._information_set.min() < 0 or self._information_set.max() > self._length:
            raise ValueError("Parameter 'information_set' must be a 'k'-subset of 'range(n)'")

        # create generator matrix
        self._parity_set = np.setdiff1d(np.arange(self._length), self._information_set)
        self._generator_matrix = np.empty((self._dimension, self._length), dtype=np.int)
        self._generator_matrix[:, self._information_set] = np.eye(self._dimension, dtype=np.int)
        self._generator_matrix[:, self._parity_set] = self._parity_sub_matrix

        # create parity check matrix
        self._parity_check_matrix = np.empty((self._redundancy, self._length), dtype=np.int)
        self._parity_check_matrix[:, self._information_set] = self._parity_sub_matrix.T
        self._parity_check_matrix[:, self._parity_set] = np.eye(self._redundancy, dtype=np.int)

        self._hamming_distance = redundancy

    @property
    def information_set(self):
        return self._information_set

    def decode(self, codeword):
        if len(codeword) != self._length:
            raise ValueError("length of message is unequal to n")
        return codeword[self.information_set]
