from copy import deepcopy
from typing import List, Dict

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'

DIRECTIONS = {'ne': (1, 1),
              'nw': (-1, 1),
              'e': (2, 0),
              'w': (-2, 0),
              'se': (1, -1),
              'sw': (-1, -1)}


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other) -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    def move(self, d: str):
        move_p = Point(*DIRECTIONS[d]) + self
        self.x, self.y = move_p.x, move_p.y

    def get_neighbors(self) -> List['Point']:
        moves = [Point(*v) for v in DIRECTIONS.values()]
        return [self + move for move in moves]


def navigate_line(line: str) -> Point:
    point = Point(0, 0)
    line_idx = 0
    while line_idx < len(line):
        if line[line_idx] in ('n', 's'):
            d = line[line_idx:line_idx + 2]
            point.move(d)
            line_idx += 2
        else:
            d = line[line_idx]
            point.move(d)
            line_idx += 1
    return point


def color(i: int) -> str:
    if i == 1:
        return 'white'
    if i == 0:
        return 'black'
    return 'WHAT!?'


def part1(lines: List[str]) -> Dict[Point, int]:
    points_found = {Point(0, 0): 1}
    for line in lines:
        end_point = navigate_line(line)
        if points_found.get(end_point) is not None:
            points_found[end_point] = points_found[end_point] ^ 1
        else:
            points_found[end_point] = 0
    # for p, c in points_found.items():
    #     print(f'{p}: {color(c)}')
    print(sum(1 for v in points_found.values() if v == 0))
    return points_found


def part2(tile_dict: Dict[Point, int], days: int):

    def count_live_neighbors(p: Point):
        count = 0
        for neighbor in p.get_neighbors():
            if tile_dict.get(neighbor) is not None and tile_dict[neighbor] == 0:
                count += 1
        return count

    with U.localtimer():
        for day in range(1, days + 1):
            new_dict = {}
            seen_today = set()
            for point in tile_dict:
                neighbors = point.get_neighbors()
                for n in [*neighbors, point]:
                    if n in seen_today:
                        continue
                    curr_color = 1 if tile_dict.get(n) is None else tile_dict[n]
                    live_neighbors = count_live_neighbors(n)
                    if (curr_color == 1 and live_neighbors == 2) or (curr_color == 0 and (0 < live_neighbors < 3)):
                        new_dict[n] = 0
                    seen_today.add(n)
            tile_dict = new_dict
    print(f'Day {day}: {sum(1 for v in tile_dict.values() if v == 0)}')


def _run_program(input_path: str):
    lines = U.read_path_lines(input_path)
    tile_dict = part1(lines)
    part2(tile_dict, 100)


def __test():
    _run_program(f'{DATA_DIR}test')


def __main():
    _run_program(f'{DATA_DIR}day24')


if __name__ == '__main__':
    # __test()
    __main()
