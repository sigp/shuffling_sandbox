"""
A shuffling implementation which doesn't read a fixed
amount of bits for each rng call, instead only reads the
minimum required bits for the specified range.
"""
import math
from bitstring import BitArray
from src.utils import keccak256


def shuffle(lst, seed):
    rng = ShuffleRng(seed)
    o = [x for x in lst]
    durstenfeld_shuffle(o, rng.rand_range)
    return o


def durstenfeld_shuffle(lst, rand_range):
    for i in range(len(lst) - 1):
        j = rand_range(i, len(lst))
        lst[i], lst[j] = lst[j], lst[i]


class ShuffleRng:
    def __init__(self, seed):
        self.seed = BitArray(keccak256(seed))
        self.seed_idx = 0

    def rehash_seed(self):
        self.seed = BitArray(keccak256(self.seed.bytes))
        self.seed_idx = 0

    def rand(self, num_bits):
        first = self.seed_idx
        last = self.seed_idx + num_bits
        if last >= len(self.seed):
            self.rehash_seed()
            return self.rand(num_bits)
        x = self.seed[first:last].uint
        self.seed_idx += num_bits
        return x

    def rand_range(self, a, b):
        n = b - a
        bits = math.ceil(math.log2(n))
        rand_max = 2**bits
        x = 0
        while True:
            x = self.rand(bits)
            if x < rand_max - rand_max % n:
                break
        return (x % n) + a
