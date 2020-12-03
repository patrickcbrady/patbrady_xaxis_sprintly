import operator
from functools import reduce
from typing import NamedTuple, List

from utils import localtimer

DATA_DIR = './inputs/'


class SlopeMap(NamedTuple):
    slope_map: List[str]

    @classmethod
    def from_file(cls, path: str) -> 'SlopeMap':
        with open(path, 'r') as f:
            return cls(f.read().split('\n'))

    @property
    def h_bound(self):
        return len(self.slope_map[0])

    @property
    def v_bound(self):
        return len(self.slope_map)

    def draw_map_divider(self):
        print('\n')
        print('*' * self.h_bound * 2)
        print('\n')

    def draw_row(self, h: int, v: int):
        h = h % self.h_bound
        row = self.slope_map[v]
        print(''.join((row[:h], row[h].replace('.', 'O').replace('#', 'X'), row[h:][1:])))

    def trees_on_slope(self, h: int, v: int, draw: bool = False):
        y = v
        x = h
        trees = 0
        while y < self.v_bound:
            if draw:
                self.draw_row(x, y)
            if self.slope_map[y][x % self.h_bound] == '#':
                trees += 1
            y += v
            x += h
        if draw:
            self.draw_map_divider()
        return trees


def part1(sm: SlopeMap):
    with localtimer():
        trees = sm.trees_on_slope(3, 1)
    print(trees)


def part2(sm: SlopeMap):
    trees = (sm.trees_on_slope(h, v) for h, v in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])
    with localtimer():
        res = reduce(operator.mul, trees)
    print(res)


def __main():
    sm = SlopeMap.from_file(f'{DATA_DIR}day3')
    part1(sm)
    part2(sm)


if __name__ == '__main__':
    __main()
