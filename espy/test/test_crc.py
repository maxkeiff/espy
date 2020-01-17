from espy.crc import *
import random
import time

random.seed(42)


def test_simple_crc_1():
    crc = CyclicRedundancyCheck(p="1100")
    assert crc.compute_crc("11001100") == "000"


def test_simple_crc_2():
    crc = CyclicRedundancyCheck(p="10011")
    assert crc.compute_crc("1101011011") == "1110"


def test_simple_crc_3():
    crc = CyclicRedundancyCheck(p="1011")
    assert crc.compute_crc("11010011101100") == "100"


def test_simple_crc_4():
    crc = CyclicRedundancyCheck(p="110101")
    assert crc.compute_crc("1101100101") == "00000"


def test_simple_crc_5():
    crc = CyclicRedundancyCheck(p="100111")
    assert crc.compute_crc("100101110011101") == "10110"


# http://mathworld.wolfram.com/IrreduciblePolynomial.html
def test_crc_decode_encode():

    polynomials = ["10", "11", "111", "1101", "1011"]
    messages = [bin(random.randint(0, 2 ** 64 - 1))[2:] for _ in range(20)]

    crcs = [CyclicRedundancyCheck(p) for p in polynomials]

    for crc in crcs:
        for message in messages:
            enc = crc.crc_encode(message)
            assert crc.crc_check(enc)


def test_predefined_crc_decode_encode():

    start = time.time()

    messages = [bin(random.randint(0, 2 ** 64 - 1))[2:] for _ in range(100)]
    crcs = [CRC_1(), CRC_2(), CRC_3(), CRC_8(), CRC_10(), CRC_12(), CRC_16(), CRC_32()]

    for crc in crcs:
        for message in messages:
            enc = crc.crc_encode(message)
            assert crc.crc_check(enc)

    end = time.time()
    total = end - start
    print("The test took {0:.6f} seconds.".format(total))
