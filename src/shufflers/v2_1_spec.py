from src.utils import blake

DEFAULT_CONFIG = "not used"


def shuffle(lst,
            seed,
            config=DEFAULT_CONFIG):
    lst_count = len(lst)
    assert lst_count <= 16777216
    o = [x for x in lst]
    source = seed
    i = 0
    while i < lst_count:
        source = blake(source)
        for pos in range(0, 30, 3):
            m = int.from_bytes(source[pos:pos+3], 'big')
            remaining = lst_count - i
            if remaining == 0:
                break
            rand_max = 16777216 - 16777216 % remaining
            if m < rand_max:
                replacement_pos = (m % remaining) + i
                o[i], o[replacement_pos] = o[replacement_pos], o[i]
                i += 1
    return o
