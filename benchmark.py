import time
import itertools
import random
import string

from src.shufflers import v2_1_spec
from src.shufflers import v2_1_spec_modified
from src.shufflers import reference
from src.utils import (blake, list_compare)

shufflers = {
    "v2.1_spec": v2_1_spec.shuffle,
    "v2.1_spec_modified": v2_1_spec_modified.shuffle,
    "pedagogical": reference.shuffle,
}

BENCHMARK_ROUNDS = 10000
LIST_SIZE = 5

lst = list(range(LIST_SIZE))

# This seed is known to cause differences between the
# v2.1 and v2.1_fixed implemenations with a list size
# of 10000
seed = blake("hq2u4v6vk17t".encode())


def benchmark_shufflers(*args, **kwargs):
    rounds = BENCHMARK_ROUNDS
    for name, func in shufflers.items():
        t1 = time.time()
        for _ in range(rounds):
            func(*args, **kwargs)
        t2 = time.time()
        avg_time = (t2 - t1) / rounds
        print("Function={:20}\tTime={}".format(name, avg_time))


def compare_outputs(*args, **kwargs):
    results = []
    for name, func in shufflers.items():
        result = func(*args, **kwargs)
        results.append((name, result))
    pairs = itertools.combinations(results, 2)
    for pair in pairs:
        a = pair[0]
        b = pair[1]
        a_name = a[0]
        a_result = a[1]
        b_name = b[0]
        b_result = b[1]
        equal = list_compare(a_result, b_result)
        symbol = "==" if equal else "!="
        print("{:20}\t{}\t{}".format(a_name, symbol, b_name))


def find_inequality(shuffler_a, shuffler_b):
    list_size = 10000
    while True:
        rand_string = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=12)
        )
        rand_bytes = rand_string.encode()
        a = shuffler_a(list(range(list_size)), blake(rand_bytes))
        b = shuffler_b(list(range(list_size)), blake(rand_bytes))
        if not list_compare(a, b):
            print(
                "Inequal with seed: blake({}), list length:{}"
                .format(rand_string, list_size)
            )


benchmark_shufflers(lst, seed)
compare_outputs(lst, seed)
# find_inequality(fixed.shuffle, separate.shuffle)
