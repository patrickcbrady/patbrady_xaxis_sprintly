from typing import List, NamedTuple, Set, Union, FrozenSet, Type

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
class World:
    active_positions: FrozenSet[Pos]

    @classmethod
    def from_str_list(cls, str_list: List[List[str]]) -> 'World':
        active = set()
        z = 0
        for y, row in enumerate(str_list):
            for x, col in enumerate(row):
                if col == '#':
                    active.add(Pos(x, y, z))
        return cls(frozenset(active))

    def is_active(self, p: Union[Pos, HyperPos]) -> bool:
        return p in self.active_positions

    def print(self):
        active_and_neighbors = {n for p in self.active_positions for n in p.get_neighbors()} | self.active_positions
        pos_z = {p.z for p in active_and_neighbors}
        pos_y = {p.y for p in active_and_neighbors}
        pos_x = {p.x for p in active_and_neighbors}
        for z in range(min(pos_z), max(pos_z) + 1):
            print(f'z: {z}')
            for y in range(min(pos_y), max(pos_y) + 1):
                row = ''
                for x in range(min(pos_x), max(pos_x) + 1):
                    if self.is_active(Pos(x, y, z)):
                        row += '#'
                    else:
                        row += '.'
                print(row)

    def count_all_active(self) -> int:
        return len(self.active_positions)

    def count_active_neighbors(self, p: Union[Pos, HyperPos]) -> int:
        return len({n for n in p.get_neighbors() if self.is_active(n)})

    def get_cycle_result(self) -> Union[Set[Pos], Set[HyperPos]]:
        snapshot = set(self.active_positions)
        active_and_neighbors = {n for p in self.active_positions for n in p.get_neighbors()} | self.active_positions
        for p in active_and_neighbors:
            active_count = self.count_active_neighbors(p)
            if self.is_active(p):
                if active_count not in range(2, 4):
                    snapshot.remove(p)
            else:
                if active_count == 3:
                    snapshot.add(p)
        return snapshot

    def run_cycle(self) -> 'World':
        return World(self.get_cycle_result())


@dataclass
class HyperWorld(World):
    active_positions: FrozenSet[HyperPos]

    @classmethod
    def from_str_list(cls, str_list: List[List[str]]) -> 'HyperWorld':
        active = set()
        w = 0
        z = 0
        for y, row in enumerate(str_list):
            for x, col in enumerate(row):
                if col == '#':
                    active.add(HyperPos(x, y, z, w))
        return cls(frozenset(active))

    def print(self):
        active_and_neighbors = {p.get_neighbors() for p in self.active_positions} | {self.active_positions}
        pos_w = {p.w for p in active_and_neighbors}
        pos_z = {p.z for p in active_and_neighbors}
        pos_y = {p.y for p in active_and_neighbors}
        pos_x = {p.x for p in active_and_neighbors}
        for w in range(min(pos_w), max(pos_w) + 1):
            for z in range(min(pos_z), max(pos_z) + 1):
                print(f'w: {w}, z: {z}')
                for y in range(min(pos_y), max(pos_y) + 1):
                    row = ''
                    for x in range(min(pos_x), max(pos_x) + 1):
                        if self.is_active(HyperPos(x, y, z, w)):
                            row += '#'
                        else:
                            row += '.'
                    print(row)

    def run_cycle(self) -> 'HyperWorld':
        return HyperWorld(frozenset(self.get_cycle_result()))


def run_world_cycles(start: List[List[str]], world_type: Type[Union[World, HyperWorld]]):
    world = world_type.from_str_list(start)
    with U.localtimer():
        for i in range(0, 6):
            # world.print()
            world = world.run_cycle()
    print(world.count_all_active())


def part1(start: List[List[str]]):
    run_world_cycles(start, World)


def part2(start: List[List[str]]):
    run_world_cycles(start, HyperWorld)


def __test():
    start = [list(s) for s in U.read_path_lines(f'{DATA_DIR}test')]
    part1(start)
    part2(start)


def __main():
    start = [list(s) for s in U.read_path_lines(f'{DATA_DIR}day17')]
    part1(start)
    part2(start)


if __name__ == '__main__':
    # __test()
    __main()
