from espy.algorithms.block_code import *
import numpy as np


assert(hamming([1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 1, 0, 0]) == [1, 1, 0, 0, 0, 1, 0])

generator = np.array(
    [
        [1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 0, 0, 0],
    ]
)

# init systematic block code with generator matrix
systematic_code = SystematicCode(generator)
print(systematic_code.__str__())
# check parity matrix
assert (
    systematic_code.parity_check_matrix
    == [[1, 1, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 1]]
).any
parity_t = systematic_code.parity_check_matrix.transpose()
assert (np.dot(generator, parity_t) % 2 == 0).any

# check encode
message = np.array([1, 0, 0, 1])
codeword = systematic_code.encode(message)
assert (codeword == [1, 0, 0, 1, 1, 1, 1]).any

# check decode
decoded_message = systematic_code.decode(codeword)
assert (decoded_message == message).any

# check code word table
codeword_table = systematic_code.codeword_table()
assert (
    codeword_table
    == [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1],
    ]
).any

# check validate
assert systematic_code.validate(codeword)
assert not systematic_code.validate([1, 1, 1, 1, 0, 0, 0])
