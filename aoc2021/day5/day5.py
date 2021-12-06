from typing import List, Callable

from utils import get_coord_line_list, Coords


def print_matrix(matrix: List[List[int]]):
    n = len(matrix)
    for i in range(n):
        line = ''.join('.' if v == 0 else str(v) for v in matrix[i])
        print(line)


def get_iter_range(num1: int, num2: int) -> range:
    return range(num1, num2 + 1) if num2 >= num1 else range(num1, num2 - 1, -1)


def count_lines(coords: List[Coords], diag: bool = False):
    max_idx = max(num for pair in coords for tup in pair for num in tup)
    matrix = [[0 for j in range(max_idx + 1)] for i in range(max_idx + 1)]
    count = 0
    for coord_line in coords:
        (x1, y1), (x2, y2) = coord_line
        if x1 == x2:
            for row in range(min(y1, y2), max(y1, y2) + 1):
                matrix[row][x1] += 1
                if matrix[row][x1] == 2:
                    count += 1
        elif y1 == y2:
            for col in range(min(x1, x2), max(x1, x2) + 1):
                matrix[y1][col] += 1
                if matrix[y1][col] == 2:
                    count += 1
        else:
            if diag:
                x_range = get_iter_range(x1, x2)
                y_range = get_iter_range(y1, y2)
                for row, col in zip(y_range, x_range):
                    matrix[row][col] += 1
                    if matrix[row][col] == 2:
                        count += 1
    return matrix, count


def run(coords: List[Coords], diag: bool = False):
    matrix, count = count_lines(coords, diag)
    print(count)
    check = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 1:
                check += 1
    print(check)
    # print_matrix(matrix)


def __test():
    coords = get_coord_line_list('test')
    # run(coords)
    run(coords, diag=True)


def __main():
    coords = get_coord_line_list('input')
    # run(coords)
    run(coords, diag=True)


if __name__ == '__main__':
    __test()
    __main()
