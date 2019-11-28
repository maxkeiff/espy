class CyclicRedundancyCheck:
    """Base class for CRC algorithms. Derive and hardcode p to define CRC versions."""

    def __init__(self, p):
        """Initializes a CRC that given a bitstream computes its residuo module p.

        Args:
            p (str): string that represents the polynomial. For example x^4+x^2+1 yields to "10101".
        """

        try:
            p = p.lstrip("0")  # Remove trailing zeros
            int(p, 2)
        except ValueError:
            raise Exception("Polynomial does not have the correct format!")

        self.n = len(p) - 1
        self.p = int(p[1:], 2)

    def compute_crc(self, a):
        """Computes the residuo r = a*x^n mod p.
        
        Args:
            a (str): string with only 0s and 1s as characters.

        Returns:
            r (str): string of residuo polynomial padded to length n
        """

        crc_register = 0

        for a_i in a:
            crc_register = crc_register << 1  # Bitshift
            outshifted_bit = crc_register >> self.n  # Compute outshifted bit
            crc_register &= 2 ** self.n - 1  # Cutoff outshifted bits
            if outshifted_bit ^ int(
                a_i, 2
            ):  # subtract if current residuo does not lead to a 0 after xor
                crc_register ^= self.p

        return bin(crc_register)[2:].zfill(self.n)

    def crc_encode(self, a):
        """Appends n redundancy bits on the message.

        Args:
            a (str): message 

        Returns:
            str: message with redundancy bits
        """

        return a + self.compute_crc(a)

    def crc_check(self, a):
        """Takes a message with CRC bits and checks if the message yields to the given CRC.

        Args:
            a (str): A bitstring with n CRC bits at the end

        Returs:
            bool: True if valid
        """

        message = a[: -self.n]
        crc = a[-self.n :]
        crc_received = self.compute_crc(message)
        return crc_received == crc
