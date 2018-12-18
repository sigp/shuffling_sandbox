from sha3 import keccak_256


def keccak256(x):
    return keccak_256(x).digest()

def list_compare(a, b):
    diff = [i for i, j in zip(a, b) if i != j]
    return len(diff) == 0
