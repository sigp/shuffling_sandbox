import time
from shufflers import original
from shufflers import fixed
from shufflers import separate
from shufflers.utils import blake

lst = list(range(10000))
seed = blake(b"1ktjd4npm46i")

a = original.shuffle(lst, seed)
b = separate.shuffle(lst, seed)


def st_time(func):
    """
        st decorator to calculate the total time of a func
    """
    def st_func(*args, **keyArgs):
        rounds = 5000
        t1 = time.time()
        for _ in range(rounds):
            r = func(*args, **keyArgs)
        t2 = time.time()
        avg_time = (t2 - t1) / rounds
        print("Function={}, Time={}".format(func.__name__, avg_time))
        return r

    return st_func


@st_time
def run_original():
    original.shuffle(lst, seed)


@st_time
def run_fixed():
    fixed.shuffle(lst, seed)


@st_time
def run_separate():
    separate.shuffle(lst, seed)


run_original()
run_fixed()
run_separate()
