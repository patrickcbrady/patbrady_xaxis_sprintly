from functools import lru_cache
from typing import Generator, Tuple

import utils as U

DATA_DIR = './inputs/'
KEY_MOD = 20201227


@lru_cache(maxsize=None)
def update_val(val: int, subject: int):
    return (val * subject) % KEY_MOD


def calc_key(subject: int = 7) -> Generator:
    v = 1
    while True:
        v = update_val(v, subject)
        yield v


def get_encryption_key(device_public_key: int, other_device_loop_size: int) -> int:
    res = 0
    encryption_calc = calc_key(device_public_key)
    for i in range(0, other_device_loop_size):
        res = next(encryption_calc)
    return res


def find_loop_size(card_key: int, door_key: int) -> Tuple[int, int]:
    """return the loop size and device index (0=card, 1=door) for the first device cracked"""
    gen = calc_key()
    size = 1
    while True:
        res = next(gen)
        if res == card_key:
            return size, 0
        elif res == door_key:
            return size, 1
        size += 1


def part1(card_key: int, door_key: int):
    with U.localtimer():
        loop_size, device_type = find_loop_size(card_key, door_key)
    key = door_key if device_type == 0 else card_key
    private_key = get_encryption_key(key, loop_size)
    print(private_key)


def _run_program(input_path: str):
    card_key, door_key = tuple(map(int, U.read_path_lines(input_path)))
    part1(card_key, door_key)


def __test():
    _run_program(f'{DATA_DIR}test')


def __main():
    _run_program(f'{DATA_DIR}day25')


if __name__ == '__main__':
    # __test()
    __main()
