import math
from typing import List, Tuple


class LavaTubes:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.low_points = set()

    @classmethod
    def from_file(cls, name: str) -> 'LavaTubes':
        with open(f'./{name}') as f:
            lines = f.read().split('\n')
            matrix = [list(map(int, line)) for line in lines]
            return cls(matrix)

    def get_neighbors(self, i: int, j: int) -> List[Tuple[int, int]]:
        return [(r, c) for r, c in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
                if self.height > r >= 0 and self.width > c >= 0]

    def is_low(self, i: int, j: int):
        neighbors = self.get_neighbors(i, j)
        return all(self.matrix[r][c] > self.matrix[i][j] for r, c in neighbors)

    def get_risk_level_sum(self):
        risk = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.is_low(i, j):
                    risk += 1 + self.matrix[i][j]
                    self.low_points.add((i, j))
        return risk

    def print(self):
        for row in self.matrix:
            print(''.join(str(i) for i in row))

    def get_basin_size(self, i: int, j: int) -> int:
        visited = set()

        def dfs(i: int, j: int):
            if (i, j) not in visited:
                visited.add((i, j))
                children = {(r, c) for r, c in self.get_neighbors(i, j)
                            if self.matrix[r][c] > self.matrix[i][j] and self.matrix[r][c] != 9}
                for c in children:
                    dfs(*c)

        dfs(i, j)
        return len(visited)

    def get_basin_size_product(self):
        if not self.low_points:
            self.get_risk_level_sum()
        sizes = []
        for i, j in self.low_points:
            sizes.append(self.get_basin_size(i, j))
        print(math.prod(sorted(sizes)[-3:]))


def part1(name: str):
    print(LavaTubes.from_file(name).get_risk_level_sum())


def part2(name: str):
    LavaTubes.from_file(name).get_basin_size_product()


def __test():
    part1('large_test')
    part2('large_test')


def __main():
    part1('input')
    part2('input')


if __name__ == '__main__':
    # __test()
    __main()
