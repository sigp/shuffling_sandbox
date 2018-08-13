try:
    from hashlib import blake2s
except:
    from pyblake2 import blake2s


def blake(x):
    return blake2s(x).digest()


def list_compare(a, b):
    diff = [i for i, j in zip(a, b) if i != j]
    return len(diff) == 0
