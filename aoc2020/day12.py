from typing import List, Tuple

from dataclasses import dataclass
from frozendict import frozendict

import utils as U

DATA_DIR = './inputs/'

THE_4_WINDS = frozendict({'E': (1, 0),
                          'N': (0, 1),
                          'W': (-1, 0),
                          'S': (0, -1)})


@dataclass
class NavGrid:
    moves: List[str]
    pos: Tuple[int, int] = (0, 0)
    waypoint_pos: Tuple[int, int] = (10, 1)
    dir: int = 0

    @property
    def vec(self) -> Tuple[int, int]:
        """
        return the directional vector based on the direction that the ship is facing
        0 - east, 1 - north, 2 - west, 3 - south
        """
        vectors = list(THE_4_WINDS.values())
        return vectors[self.dir]

    @staticmethod
    def get_turns(ori: str, deg: int) -> int:
        """return the number of leftward turns to make"""
        mul = 1 if ori == 'L' else -1
        return (deg // 90) * mul

    def rotate(self, ori: str, deg: int):
        turns = self.get_turns(ori, deg)
        self.dir = (self.dir + turns) % 4

    def rotate_waypoint(self, ori: str, deg: int):
        e, n = self.waypoint_pos
        locations = [(e, n), (-n, e), (-e, -n), (n, -e)]
        turns = self.get_turns(ori, deg) % 4
        self.waypoint_pos = locations[turns]

    @staticmethod
    def move_object(pos: Tuple[int, int], vec: Tuple[int, int], units: int) -> Tuple[int, int]:
        e, n = vec
        move = (e * units, n * units)
        return tuple(map(sum, zip(pos, move)))

    def move_ship(self, ori: str, units: int):
        vec = self.vec if ori == 'F' else THE_4_WINDS[ori]
        self.pos = self.move_object(self.pos, vec, units)

    def move_waypoint(self, ori: str, units: int):
        vec = THE_4_WINDS[ori]
        self.waypoint_pos = self.move_object(self.waypoint_pos, vec, units)

    def move_ship_to_waypoint(self, times: int):
        self.pos = self.move_object(self.pos, self.waypoint_pos, times)

    def run_moves(self):
        for m in self.moves:
            ori, amp = m[0], int(m[1:])
            if ori in ['L', 'R']:
                self.rotate(ori, amp)
            else:
                self.move_ship(ori, amp)

    def run_waypoint_moves(self):
        for m in self.moves:
            ori, amp = m[0], int(m[1:])
            if ori in ['L', 'R']:
                self.rotate_waypoint(ori, amp)
            elif ori == 'F':
                self.move_ship_to_waypoint(amp)
            else:
                self.move_waypoint(ori, amp)

    def print_status(self):
        print(f'ship pos: {self.pos}')
        print(f'waypoint pos: {self.waypoint_pos}')

    @property
    def manhattan_dist(self):
        """return the current position's manhattan distance from origin 0, 0"""
        e, n = self.pos
        return abs(e) + abs(n)


def part1(data: List[str]):
    ng = NavGrid(data)
    ng.run_moves()
    print(ng.manhattan_dist)


def part2(data: List[str]):
    ng = NavGrid(data)
    ng.run_waypoint_moves()
    print(ng.manhattan_dist)


def __main():
    data = U.read_path_lines(f'{DATA_DIR}day12')
    part1(data)
    part2(data)


if __name__ == '__main__':
    __main()
