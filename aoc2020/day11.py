import copy
from functools import lru_cache
from itertools import product
from typing import List, Tuple, Optional

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'

the_8_winds = frozenset((r, c) for r, c in product(range(-1, 2), range(-1, 2))) - {(0, 0)}


@dataclass
class SeatArrangement:
    rows: List[List[str]]

    @property
    def v_size(self):
        return len(self.rows)

    @property
    def h_size(self):
        return len(self.rows[0])

    def count_occupied(self, row: int, col: int, count_visible: bool = False) -> int:
        def is_occupied(seat: Tuple[int, int]) -> bool:
            r, c = seat
            return self.rows[r][c] == '#'

        return sum(map(is_occupied, self.get_seats_to_check(row, col, count_visible)))

    # trade memory for speed
    @lru_cache(maxsize=None)
    def get_seats_to_check(self, row: int, col: int, count_visible: bool) -> List[Tuple[int, int]]:
        res = []
        for v, h in the_8_winds:
            if count_visible:
                seat_pos = self.get_visible_seat(row, col, (v, h))
                if seat_pos is not None:
                    res.append(seat_pos)
            else:
                r = row + v
                c = col + h
                if (0 <= r < self.v_size) and (0 <= c < self.h_size):
                    res.append((r, c))
        return res

    # here's where we really avoid duplicate work
    @lru_cache(maxsize=None)
    def get_visible_seat(self, row: int, col: int, direction: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        v, h = direction
        new_row = row + v
        new_col = col + h
        if not ((0 <= new_row < self.v_size) and (0 <= new_col < self.h_size)):
            return None
        if self.rows[new_row][new_col] != '.':
            return new_row, new_col
        else:
            return self.get_visible_seat(new_row, new_col, direction)

    def print(self):
        for r in self.rows:
            print(''.join(r))

    def apply_rules(self, check_visible: bool = False, tolerance: int = 4) -> Tuple[bool, int]:
        """return True if rules cause a change, False if state stays the same"""
        new_rows = copy.deepcopy(self.rows)

        def get_occupied(r: int, c: int) -> int:
            return self.count_occupied(r, c, check_visible)

        occupancy = 0
        for i, row in enumerate(self.rows):
            for j, seat in enumerate(row):
                if seat == 'L':
                    if get_occupied(i, j) == 0:
                        new_rows[i][j] = '#'
                        occupancy += 1
                elif seat == '#':
                    if get_occupied(i, j) >= tolerance:
                        new_rows[i][j] = 'L'
                    else:
                        occupancy += 1
        if new_rows != self.rows:
            self.rows = new_rows
            return True, occupancy
        else:
            return False, occupancy

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __hash__(self):
        return hash(type(self))


def part1(data: List[List[str]]):
    sa = SeatArrangement(data)
    with U.localtimer():
        while True:
            has_changed, seats_occupied = sa.apply_rules()
            if not has_changed:
                break
    print(seats_occupied)


def part2(data: List[List[str]]):
    sa = SeatArrangement(data)
    with U.localtimer():
        while True:
            has_changed, seats_occupied = sa.apply_rules(check_visible=True, tolerance=5)
            if not has_changed:
                break
    print(seats_occupied)


def __main():
    data = [list(r) for r in U.read_path_lines(f'{DATA_DIR}day11')]
    part1(data)
    part2(data)


if __name__ == '__main__':
    __main()
