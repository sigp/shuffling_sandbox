import time
import itertools
import random
import string
import argparse
import yaml

from src.shufflers import v2_1_spec
from src.shufflers import reference
from src.shufflers import bitsipper
from src.utils import (blake, list_compare)

shufflers = {
    "v2.1_spec": v2_1_spec.shuffle,
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
    "print",
    "test_vectors",
)

parser = argparse.ArgumentParser(description='Sandbox for testing shuffling functions.')
parser.add_argument('method', metavar='METHOD', type=str, choices=METHODS,
                    help='The task to be executed. Options: {}'.format(METHODS))
parser.add_argument('--list-size', dest='list_size',
                    type=int, default=1000,
                    help='Length of list to be sorted.')
parser.add_argument('--seed', dest='seed_str',
                    type=str, default="4kn4driuctg8",
                    help='Initial seed (not used for fuzzing)')
parser.add_argument('--rounds', dest='rounds',
                    type=int, default=10000,
                    help='Number of rounds when benchmarking.')

args = parser.parse_args()

# this seed is know to cause inequality between the
# v2.1 and v2.1_modified functions with a list size of 6.
seed = blake(args.seed_str.encode())

lst = list(range(args.list_size))

if args.method == "benchmark":
    benchmark_shufflers(args.rounds, lst, seed)
elif args.method == "compare":
    compare_outputs(lst, seed)
elif args.method == "inequality_fuzz":
    shufflers.pop("bitsipper")  # this shuffler will always be different
    print("Fuzz targets:")
    for shuffler in shufflers:
        print(" - {}".format(shuffler))
    while True:
        fuzz(args.list_size, shufflers)
elif args.method == "print":
    print("PARAMS: list_size: {}, seed_str: {}".format(len(lst), args.seed_str))
    print("")
    for k, v in shufflers.items():
        print("{}:\n{}\n----".format(k, v(lst, seed)))
elif args.method == "test_vectors":
    shuffler_name = "v2.1_spec"
    shuffler = shufflers[shuffler_name]
    results = []

    seeds = [
        b"",
        blake("4kn4driuctg8".encode()),     # known to cause conflicts with old shuffler
        blake("ytre1p".encode()),
        blake("mytobcffnkvj".encode()),
        blake("myzu3g7evxp5nkvj".encode()),
        blake("xdpli1jsx5xb".encode()),
        blake("oab3mbb3xe8qsx5xb".encode()),
    ]
    lists = [
        [],
        [0],
        [255],
        [4, 6, 2, 6, 1, 4, 6, 2, 1, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        [65, 6, 2, 6, 1, 4, 6, 2, 1, 5],
    ]

    shuffler = shufflers["v2.1_spec"]

    for seed in seeds:
        for lst in lists:
            output = shuffler(lst, seed)
            results.append({"seed": seed, "input": lst, "output": output})

    body = {
        "test_cases": results
    }

    with open("shuffle_test_vectors.yaml", "w") as f:
        f.write("title: Shuffling Algorithm Tests\n")
        f.write("summary: Test vectors for shuffling a list based upon a seed.\n")
        f.write("test_suite: Shuffling\n")
        f.write("\n")
        noalias_dumper = yaml.dumper.Dumper
        noalias_dumper.ignore_aliases = lambda self, data: True
        yaml.dump(body, f, Dumper=noalias_dumper)
