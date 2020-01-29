from espy.algorithms.block_code import *

# calculates the hamming distance between two vectors
assert (hamming([1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 1, 0, 0]) == 3)

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

# check hamming distance
assert (systematic_code.hamming_distance == 1)

generator = np.array(
    [
        [0, 1, 1, 0, 1, 1, 0],
        [1, 1, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 1, 0, 0, 0],
    ]
)

print('\n')

# check hamming code
hamming_code = HammingCode(3)
print(hamming_code)

codeword = hamming_code.encode(np.array([1, 0, 1, 1]))
assert all(codeword == [1, 0, 1, 1, 0, 1, 0])
message = hamming_code.decode(np.array([0, 1, 0, 0, 0, 1, 1]))
assert all(message == [0, 1, 0, 0])
message = hamming_code.decode(np.array([1, 0, 1, 1, 0, 1, 0]))
assert all(message == [1, 0, 1, 1])


# check maximum likelihood decoding
assert (hamming_code.maximum_likelihood_decode([1, 0, 1, 1, 0, 1, 1]) == np.array([1, 0, 1, 1, 0, 1, 0])).any
