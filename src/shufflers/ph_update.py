'''
This is the version of the shuffler on beacon_chain pull-request #55 at commit
8c6b18d.

https://github.com/ethereum/eth2.0-specs/pull/55/files#diff-68116df8e39118db1b49250a6a0a49cdR346
'''


from src.utils import blake

hash = blake


def shuffle(values, seed):
    """
    def shuffle(values: List[Any],
                seed: Hash32) -> List[Any]:
    """
    """
    Returns the shuffled ``values`` with seed as entropy.
    """
    values_count = len(values)

    # Entropy is consumed from the seed in 3-byte (24 bit) chunks.
    rand_max = 2 ** 24 - 1
    assert values_count < rand_max

    output = [x for x in values]
    source = seed
    index = 0
    while index < values_count - 1:
        # Re-hash the source
        source = hash(source)
        for position in range(0, 30, 3):  # Reads indices 3 bytes at a time
            # Determine the number of indices remaining and exit once the last
            # index is reached.
            remaining = values_count - index
            if remaining == 1:
                break

            # Read 3-bytes of the seed as a 24-bit big-endian integer.
            sample_from_source = int.from_bytes(source[position:position + 3], 'big')

            # Sample values greater than or equal to `sample_max` will cause
            # modulo bias when mapped into the `remaining` range.
            sample_max = rand_max - rand_max % remaining

            # Perform a swap if the consumed entropy will not cause modulo bias.
            if sample_from_source < sample_max:
                # Select a replacement index for the present index.
                replacement_position = (sample_from_source % remaining) + index
                # Swap the present index with the replacement index.
                output[index], output[replacement_position] = output[replacement_position], output[index]
                index += 1
            else:
                # The sample causes modulo bias. A new sample should be read.
                pass

    return output
