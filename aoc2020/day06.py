from functools import reduce

import utils as U
from typing import List

DATA_DIR = './inputs/'


def count_yes(answers: List[str]) -> int:
    return sum((len(set(ans)) for ans in answers))


def count_all_grp_yes(grp_answers: List[str]):
    return sum([len(reduce(set.intersection, [set(a) for a in grp.split(' ')])) for grp in grp_answers])


def part1(answers: List[str]):
    print(count_yes(answers))


def part2(grp_answers: List[str]):
    print(count_all_grp_yes(grp_answers))


def __main():
    ans_groups = U.read_path_blank_lines(f'{DATA_DIR}day6')
    answers = [a.replace(' ', '') for a in ans_groups]
    part1(answers)
    part2(ans_groups)


if __name__ == '__main__':
    __main()
