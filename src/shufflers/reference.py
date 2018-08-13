from src.utils import blake

NUM_RAND_BITS = 24


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
        self.seed = blake(seed)
        self.seed_idx = 0

    def rehash_seed(self):
        self.seed = blake(self.seed)
        self.seed_idx = 0

    def rand(self):
        num_bytes = int(NUM_RAND_BITS / 8)
        first = self.seed_idx
        last = self.seed_idx + num_bytes
        if last >= len(self.seed):
            self.rehash_seed()
            return self.rand()
        x = int.from_bytes(self.seed[first:last], 'big')
        self.seed_idx += num_bytes
        return x

    def rand_range(self, a, b):
        rand_max = 2**NUM_RAND_BITS
        n = b - a
        x = 0
        while True:
            x = self.rand()
            if x < rand_max - rand_max % n:
                break
        return (x % n) + a
