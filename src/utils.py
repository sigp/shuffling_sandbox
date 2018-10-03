try:
    from hashlib import blake2b
except Exception:
    from pyblake2 import blake2b


def blake(x):
    return blake2b(x).digest()[:32]


def list_compare(a, b):
    diff = [i for i, j in zip(a, b) if i != j]
    return len(diff) == 0
