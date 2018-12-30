from src.utils import keccak256

NUM_RAND_BITS = 24
RAND_MAX = 2**NUM_RAND_BITS - 1


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
        self.seed = keccak256(seed)
        self.seed_idx = 0

    def rehash_seed(self):
        self.seed = keccak256(self.seed)
        self.seed_idx = 0

    def rand(self):
        num_bytes = int(NUM_RAND_BITS / 8)
        first = self.seed_idx
        last = self.seed_idx + num_bytes
        if last > len(self.seed):
            self.seed = keccak256(self.seed)
            self.seed_idx = 0
            first = self.seed_idx
            last = self.seed_idx + num_bytes
        x = int.from_bytes(self.seed[first:last], 'big')
        self.seed_idx += num_bytes
        return x

    def rand_range(self, a, b):
        n = b - a
        x = 0
        while True:
            x = self.rand()
            if x < RAND_MAX - RAND_MAX % n:
                break
        return (x % n) + a
