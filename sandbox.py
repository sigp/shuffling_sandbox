import time
import itertools
import random
import string
import argparse

from src.shufflers import v2_1_spec
from src.shufflers import v2_1_spec_modified
from src.shufflers import reference
from src.utils import (blake, list_compare)

shufflers = {
    "v2.1_spec": v2_1_spec.shuffle,
    "v2.1_spec_modified": v2_1_spec_modified.shuffle,
    "pedagogical": reference.shuffle,
}


def benchmark_shufflers(rounds, *args, **kwargs):
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


"""
Begin argument parsing
"""

METHODS = (
    "benchmark",
    "compare",
)

parser = argparse.ArgumentParser(description='Sandbox for testing shuffling functions.')
parser.add_argument('method', metavar='METHOD', type=str, choices=METHODS,
                    help='The task to be executed. Options: {}'.format(METHODS))
parser.add_argument('--list-size', dest='list_size',
                    type=int, default=1000,
                    help='Length of list to be sorted.')
parser.add_argument('--rounds', dest='rounds',
                    type=int, default=10000,
                    help='Number of rounds when benchmarking.')

args = parser.parse_args()

seed = blake("hq2u4v6vk17t".encode())

lst = list(range(args.list_size))

if args.method == "benchmark":
    benchmark_shufflers(args.rounds, lst, seed)
elif args.method == "compare":
    compare_outputs(lst, seed)
