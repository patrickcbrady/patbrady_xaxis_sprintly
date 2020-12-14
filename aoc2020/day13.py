from functools import reduce
from typing import List, Tuple

import utils as U

DATA_DIR = './inputs/'


def chinese_remainder(primes, modulos):
    sum = 0
    prod = reduce(lambda a, b: a * b, primes)
    for n_i, a_i in zip(primes, modulos):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def time_range_matches(time_bus: List[Tuple[int, int]]) -> bool:
    print([t % b for t, b in time_bus])
    return all(t % b == 0 for t, b in time_bus)


def part1(time: int, ids: List[int]):
    wait_time, bus_id = min((i * (time // i + 1) - time, i) for i in ids)
    print(wait_time * bus_id)


def part2(ids: List[str]):
    offset_ids = [(int(b) - i, int(b)) for i, b in enumerate(ids) if b != 'x']
    print(offset_ids)
    offsets = [i for i, b in offset_ids]
    buses = [b for i, b in offset_ids]
    print(offsets, buses)
    print(chinese_remainder(buses, offsets))


def __test():
    # tests = ['7,13,x,x,59,x,31,19', '67,7,59,61', '67,x,7,59,61', '67,7,x,59,61', '1789,37,47,1889']
    tests = ['1789,37,47,1889']
    for t in tests:
        part2(t.split(','))


def __main():
    time, ids = tuple(U.read_path_lines(f'{DATA_DIR}day13'))
    part1(int(time), [int(i) for i in ids.split(',') if i != 'x'])
    part2(ids.split(','))


if __name__ == '__main__':
    # __test()
    __main()
