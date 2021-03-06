# Shuffling Sandbox

A "sandbox" for testing shuffling functions for the Ethereum Beacon chain.

It contains a few shuffling functions and tools to benchmark them and compare
their results.

## Usage

Run `pip install -r requirements.txt` to get Python dependencies.

There are presently three features: `benchmark`, `compare` and `inequality_fuzz`

### Benchmark

Runs all shufflers in the `shufflers` list using the same inputs. Outputs the
times per shuffle (averaged across number of rounds).

Example:
```
$ python sandbox.py benchmark --rounds 1000 --list-size 1000

Function=v2.1_spec           	Time=0.0005764639377593994
Function=v2.1_spec_modified  	Time=0.0006669130325317383
Function=reference           	Time=0.0015188314914703369

```

### Compare

Runs all shufflers in the `shufflers` list using the same inputs and compares
the results. Outputs a indicating whether or not the shuffling functions return
the same result (list).

Example:
```
$ python sandbox.py compare --list-size 1000

v2.1_spec           	!=	v2.1_spec_modified
v2.1_spec           	!=	reference
v2.1_spec_modified  	==	reference
```

### Inequality Fuzz

Runs an endless loop which randomizes the seed and list size (within the
specified bound) and prints out a report if there is a difference found in the
results. This is useful for fuzz testing multiple implementations which should
return the same result.

Example:
```
$ python sandbox.py inequality_fuzz --list-size 1000

Inequality found! rand_string: y1zqp70s84q3, list_size: 294,  shuffler_a: v2.1_spec, shuffler_b: v2.1_spec_modified
```

### Print

Runs each shuffler with the specified list size. Outputs the shuffled list.
Useful for testing implementations in other languages.

Example:
```
$ python sandbox.py print --list-size 12

PARAMS: list_size: 12, seed_str: 4kn4driuctg8

v2.1_spec:
[3, 2, 5, 8, 4, 7, 9, 1, 0, 10, 11, 6]
----
v2.1_spec_modified:
[7, 4, 8, 6, 5, 3, 0, 11, 1, 2, 10, 9]
----
reference:
[7, 4, 8, 6, 5, 3, 0, 11, 1, 2, 10, 9]
----
bitsipper:
[8, 0, 1, 7, 6, 5, 3, 10, 4, 2, 9, 11]
----
```


## Shuffler Implementations

 - `src/shufflers/v2_1_spec.py`: the implementation from the beacon_chain
   specification.
 - `src/shufflers/v2_1_spec_modified.py`: the implementation from the
   beacon_chain specification modified fix some perceived bugs.
 - `src/shufflers/reference.py`: a reference implementation, designed for
   readability.
 - `src/shufflers/bitsipper.py`: a modified version of the reference version
 which uses the minimum required amount of bits during each rng call. Is slow.
