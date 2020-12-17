from copy import deepcopy
from functools import partial
from typing import List, NamedTuple, Dict

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'

NEIGHBORS = {(x, y, z) for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1)} - {(0, 0, 0)}
HYPERNEIGHBORS = {(x, y, z, w) for x in range(-1, 2) for y in range(-1, 2)
                  for z in range(-1, 2) for w in range(-1, 2)} - {(0, 0, 0, 0)}


class HyperPos(NamedTuple):
    x: int
    y: int
    z: int
    w: int

    def get_neighbors(self):
        return {self + HyperPos(*n) for n in HYPERNEIGHBORS}

    def __add__(self, other):
        return HyperPos(*(s + o for s, o in zip(self, other)))

    def __eq__(self, other):
        return all(s == o for s, o in zip(self, other))


class Pos(NamedTuple):
    x: int
    y: int
    z: int

    def get_neighbors(self):
        return {self + Pos(*n) for n in NEIGHBORS}

    def __add__(self, other):
        return Pos(*(s + o for s, o in zip(self, other)))

    def __sub__(self, other):
        return Pos(*(s - o for s, o in zip(self, other)))

    def __eq__(self, other):
        return all(s == o for s, o in zip(self, other))


@dataclass
class HyperWorld:
    grid: Dict[int, Dict[int, Dict[int, Dict[int, str]]]]

    @classmethod
    def from_str_list(cls, str_list: List[List[str]]) -> 'HyperWorld':
        w = 0
        z = 0
        grid = {w: {z: {}}}
        for y, row in enumerate(str_list):
            grid[w][z][y] = {}
            for x, col in enumerate(row):
                grid[w][z][y][x] = col
        return cls(grid)

    def get_active_neighbor_counts(self) -> Dict[HyperPos, int]:
        """count active neighbors for each position in the grid, causing the grid to expand to encompass neighbors"""
        ac = {}
        snapshot = deepcopy(self.grid)
        for w, hyperplane in snapshot.items():
            for z, plane in hyperplane.items():
                for y, line in plane.items():
                    for x, state in line.items():
                        pos = HyperPos(x, y, z, w)
                        ac[pos] = list(map(self.is_active, pos.get_neighbors())).count(True)
        return ac

    def is_active(self, p: HyperPos) -> bool:
        return self.read_pos(p) == '#'

    def read_pos(self, p: HyperPos) -> str:
        if self.grid.get(p.w) is None:
            self.grid[p.w] = {}
        if self.grid[p.w].get(p.z) is None:
            self.grid[p.w][p.z] = {}
        if self.grid[p.w][p.z].get(p.y) is None:
            self.grid[p.w][p.z][p.y] = {}
        if self.grid[p.w][p.z][p.y].get(p.x) is None:
            self.grid[p.w][p.z][p.y][p.x] = '.'
        return self.grid[p.w][p.z][p.y][p.x]

    def write_pos(self, p: HyperPos, state: str):
        self.read_pos(p)
        self.grid[p.w][p.z][p.y][p.x] = state

    def print(self):
        for w in self.grid:
            for z in self.grid[w]:
                print(f'z: {z}, w: {w}')
                for y in self.grid[w][z]:
                    print(''.join([c for c in self.grid[w][z][y].values()]))

    def count_all_active(self) -> int:
        return [self.is_active(HyperPos(x, y, z, w)) for w in self.grid for z in self.grid[w]
                for y in self.grid[w][z] for x in self.grid[w][z][y]].count(True)

    def run_cycle(self) -> 'HyperWorld':
        active_counts = self.get_active_neighbor_counts()
        snapshot = deepcopy(self.grid)
        new_world = HyperWorld(deepcopy(self.grid))
        for w, hyperplane in snapshot.items():
            for z, plane in hyperplane.items():
                for y, line in plane.items():
                    for x, state in line.items():
                        pos = HyperPos(x, y, z, w)
                        active_neighbors = active_counts.get(pos)
                        if active_neighbors is None:
                            active_neighbors = list(map(self.is_active, pos.get_neighbors())).count(True)
                        if self.is_active(pos):
                            if active_neighbors not in range(2, 4):
                                new_world.write_pos(pos, '.')
                        else:
                            if active_neighbors == 3:
                                new_world.write_pos(pos, '#')
        return new_world


@dataclass
class World:
    grid: Dict[int, Dict[int, Dict[int, str]]]

    @classmethod
    def from_str_list(cls, str_list: List[List[str]]) -> 'World':
        z = 0
        grid = {z: {}}
        for y, row in enumerate(str_list):
            grid[z][y] = {}
            for x, col in enumerate(row):
                grid[z][y][x] = col
        return cls(grid)

    def to_str_list(self) -> List[List[str]]:
        return [[self.grid[z][y][x] for x in self.grid[z][y]] for z in self.grid for y in self.grid[z]]

    def is_active(self, p: Pos) -> bool:
        """
        return True if cube at position is active
        """
        return self.read_pos(p) == '#'

    def print(self):
        for z in self.grid:
            print(f'z: {z}')
            for y in self.grid[z]:
                print(''.join([c for c in self.grid[z][y].values()]))

    def count_all_active(self):
        return [self.is_active(Pos(x, y, z)) for z in self.grid for y in self.grid[z] for x in self.grid[z][y]].count(True)

    def get_active_neighbor_counts(self):
        """count active neighbors for each position in the grid, causing the grid to expand to encompass neighbors"""
        ac = {}
        snapshot = deepcopy(self.grid)
        for z, plane in snapshot.items():
            for y, line in plane.items():
                for x, state in line.items():
                    pos = Pos(x, y, z)
                    ac[pos] = list(map(self.is_active, pos.get_neighbors())).count(True)
        return ac

    def read_pos(self, p: Pos) -> str:
        """
        return cube state at position in grid
        if position has never been seen, mark the cube there as inactive first
        """
        if self.grid.get(p.z) is None:
            self.grid[p.z] = {}
        if self.grid[p.z].get(p.y) is None:
            self.grid[p.z][p.y] = {}
        if self.grid[p.z][p.y].get(p.x) is None:
            self.grid[p.z][p.y][p.x] = '.'
        return self.grid[p.z][p.y][p.x]

    def write_pos(self, p: Pos, state: str):
        self.read_pos(p)
        self.grid[p.z][p.y][p.x] = state

    def run_cycle(self) -> 'World':
        active_counts = self.get_active_neighbor_counts()
        snapshot = deepcopy(self.grid)
        new_world = World(deepcopy(self.grid))
        for z, plane in snapshot.items():
            for y, line in plane.items():
                for x, state in line.items():
                    pos = Pos(x, y, z)
                    active_neighbors = active_counts.get(pos)
                    if active_neighbors is None:
                        active_neighbors = list(map(self.is_active, pos.get_neighbors())).count(True)
                    if self.is_active(pos):
                        if active_neighbors not in range(2, 4):
                            new_world.write_pos(pos, '.')
                    else:
                        if active_neighbors == 3:
                            new_world.write_pos(pos, '#')
        return new_world


def part1(start: List[List[str]]):
    world = World.from_str_list(start)
    for i in range(0, 6):
        # world.print()
        world = world.run_cycle()
    print(world.count_all_active())


def part2(start: List[List[str]]):
    world = HyperWorld.from_str_list(start)
    with U.localtimer():
        for i in range(0, 6):
            # world.print()
            world = world.run_cycle()
    print(world.count_all_active())


def __test():
    start = [list(s) for s in U.read_path_lines(f'{DATA_DIR}test')]
    # part1(start)
    part2(start)


def __main():
    start = [list(s) for s in U.read_path_lines(f'{DATA_DIR}day17')]
    # part1(start)
    part2(start)


if __name__ == '__main__':
    """43 seconds baby!"""
    # __test()
    __main()
