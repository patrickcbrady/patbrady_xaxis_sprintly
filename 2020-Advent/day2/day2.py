import re
from typing import List, Callable, Tuple

from utils import read_path_lines, localtimer

DATA_DIR = './'


def parse_row(row: str) -> Tuple[int, int, str, str]:
    # saw this one on the solutions thread and like its compactness
    left, right, char, pwd = re.split('-| |: ', row)
    return int(left), int(right), char, pwd

    # this one is faster but ugly
    # dash = row.index('-')
    # space = row.index(' ')
    # colon = row.index(':')
    # return int(row[0:dash]), int(row[dash+1:space]), row[space+1], row[colon+2:]

    # this was the first solution I used
    # policy, pwd = tuple(row.split(': '))
    # num_range, char = tuple(policy.split(' '))
    # left, right = tuple(num_range.split('-'))
    # return int(left), int(right), char, pwd


def is_valid_by_char_count(row: str) -> bool:
    """return True if the number of occurrences of char in pwd is within the bounds of min and max"""
    left, right, char, pwd = parse_row(row)
    return left <= pwd.count(char) <= right


def is_valid_by_pos(row: str) -> bool:
    """return True if char is at the 1-based position in pwd given by left or right, but not both"""
    left, right, char, pwd = parse_row(row)
    return (pwd[left-1] == char) != (pwd[right-1] == char)


def count_valid(rows: List[str], validator: Callable) -> int:
    return sum(map(validator, rows))


def part1(rows: List[str]):
    with localtimer():
        total = count_valid(rows, is_valid_by_char_count)
    print(f'Number of valid rows: {total}')


def part2(rows: List[str]):
    with localtimer():
        total = count_valid(rows, is_valid_by_pos)
    print(f'Number of valid rows: {total}')


def __main():
    # rows = read_path_lines(f'{DATA_DIR}test_input')
    rows = read_path_lines(f'{DATA_DIR}input')
    part1(rows)
    part2(rows)


if __name__ == '__main__':
    __main()
