import time
import itertools
import random
import string
import argparse

from src.shufflers import v2_1_spec
from src.shufflers import v2_1_spec_modified
from src.shufflers import reference
from src.shufflers import bitsipper
from src.utils import (blake, list_compare)

shufflers = {
    "v2.1_spec": v2_1_spec.shuffle,
    "v2.1_spec_modified": v2_1_spec_modified.shuffle,
    "reference": reference.shuffle,
    "bitsipper": bitsipper.shuffle,
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


def fuzz(max_list_size, shufflers):
    tuples = [(k, v) for k, v in shufflers.items()]
    pairs = itertools.combinations(tuples, 2)
    rand_string = ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=12)
    )
    rand_bytes = rand_string.encode()
    list_size = random.randint(1, max_list_size)
    for pair in pairs:
        shuffler_a_name = pair[0][0]
        shuffler_a_func = pair[0][1]
        shuffler_b_name = pair[1][0]
        shuffler_b_func = pair[1][1]
        a = shuffler_a_func(list(range(list_size)), blake(rand_bytes))
        b = shuffler_b_func(list(range(list_size)), blake(rand_bytes))
        if not list_compare(a, b):
            print(("Inequality found! rand_string: {}, list_size: {}, " +
                   " shuffler_a: {}," + " shuffler_b: {}")
                  .format(
                      rand_string,
                      list_size,
                      shuffler_a_name,
                      shuffler_b_name
                  ))


"""
Begin argument parsing
"""

METHODS = (
    "benchmark",
    "compare",
    "inequality_fuzz",
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

# this seed is know to cause inequality between the
# v2.1 and v2.1_modified functions with a list size of 6.
seed_str = "4kn4driuctg8"
seed = blake(seed_str.encode())

lst = list(range(args.list_size))

if args.method == "benchmark":
    benchmark_shufflers(args.rounds, lst, seed)
elif args.method == "compare":
    compare_outputs(lst, seed)
elif args.method == "inequality_fuzz":
    shufflers.pop("v2.1_spec")  # this shuffler will always be different
    shufflers.pop("bitsipper")  # this shuffler will always be different
    while True:
        fuzz(args.list_size, shufflers)
