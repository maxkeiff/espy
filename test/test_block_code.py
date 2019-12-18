from espy.block_code import *
import numpy as np

generator = np.array([[1, 0, 0, 0, 1, 1, 0],
                      [0, 1, 0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0, 1, 1],
                      [0, 0, 0, 1, 0, 0, 0]])

# init systematic block code with generator matrix
systematic_code = SystematicCode(generator)
print(systematic_code.__str__())

# encode
message = np.array([1, 0, 0, 1])
codeword = systematic_code.encode(message)
assert(codeword == [1, 0, 0, 1, 1, 1, 1]).any

# decode
decoded_message = systematic_code.decode(codeword)
assert(decoded_message == message).any

# code word table
codeword_table = systematic_code.codeword_table()
assert(codeword_table == [[0, 0, 0, 0, 0, 0, 0],
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
                          [1, 1, 1, 1, 0, 0, 1]]).any

