from functools import lru_cache
from typing import List

from utils import get_int_list_from_csv

NEW_COOLDOWN = 8
RESET_COOLDOWN = 6


@lru_cache
def calc_fish_spawned(init: int, start_day: int, end_day: int):
    count = 0
    curr_day = start_day + init + 1
    while curr_day <= end_day:
        count += 1
        count += calc_fish_spawned(NEW_COOLDOWN, curr_day, end_day)
        curr_day += RESET_COOLDOWN + 1
    return count


def run(fish: List[int], days: int):
    print(len(fish) + sum(calc_fish_spawned(f, 0, days) for f in fish))


def __test():
    fish = get_int_list_from_csv('test')
    # days = 80
    days = 256
    run(fish, days)


def __main():
    fish = get_int_list_from_csv('input')
    # days = 80
    days = 256
    run(fish, days)


if __name__ == '__main__':
    # __test()
    __main()
