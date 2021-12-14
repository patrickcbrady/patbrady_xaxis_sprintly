from typing import List


class OctoMatrix:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.has_flashed = set()
        self.flash_count = 0

    @classmethod
    def from_file(cls, name: str):
        with open(f'./{name}') as f:
            lines = f.read().split('\n')
            return cls([[int(i) for i in line] for line in lines])

    def print(self):
        for r in self.matrix:
            print(''.join(map(str, r)))

    def flash(self, i: int, j: int):
        self.has_flashed.add((i, j))
        neighbors = {(r, c) for r in range(i - 1, i + 2) for c in range(j - 1, j + 2)} - self.has_flashed
        for r, c in neighbors:
            if 0 <= r < self.height and 0 <= c < self.width:
                self.matrix[r][c] += 1
                if self.matrix[r][c] == 10:
                    self.flash(r, c)

    def do_step(self):
        self.has_flashed = set()
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j] += 1
                if self.matrix[i][j] == 10:
                    self.flash(i, j)
        self.flash_count += len(self.has_flashed)
        for i, j in self.has_flashed:
            self.matrix[i][j] = 0


def count_flashes(file: str, steps: int):
    octos = OctoMatrix.from_file(file)
    for i in range(steps):
        octos.do_step()
    print(octos.flash_count)


def find_first_sync(file: str):
    octos = OctoMatrix.from_file(file)
    size = octos.width * octos.height
    prev_count = 0
    steps = 0
    while octos.flash_count - prev_count < size:
        prev_count = octos.flash_count
        octos.do_step()
        steps += 1
    print(steps)


def __test():
    count_flashes('test', 100)
    find_first_sync('test')


def __main():
    count_flashes('input', 100)
    find_first_sync('input')


if __name__ == '__main__':
    # __test()
    __main()
