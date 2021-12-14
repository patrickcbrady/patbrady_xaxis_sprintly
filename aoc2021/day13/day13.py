from typing import List, Tuple, Set

Coord = Tuple[int, int]
Fold = Tuple[str, int]
CoordSet = Set[Coord]
FoldList = List[Fold]


def print_coords(coords: CoordSet):
    max_row = max(y for _, y in coords)
    max_col = max(x for x, _ in coords)
    matrix = [['.'] * (max_col + 1) for i in range(max_row + 1)]
    for x, y in coords:
        matrix[y][x] = '#'
    for row in matrix:
        print(''.join(row))


def get_hashes_and_folds(name: str) -> Tuple[CoordSet, FoldList]:
    with open(f'./{name}') as f:
        lines = f.read().split('\n')
        break_point = lines.index('')
        coord_lines = set()
        for s in lines[:break_point]:
            x, y = tuple(map(int, s.split(',')))
            coord_lines.add((x, y))
        fold_start = len('fold along ')
        fold_lines = [s[fold_start:].split('=') for s in lines[break_point + 1:]]
        fold_lines = list(map(lambda fold: (fold[0], int(fold[1])), fold_lines))
        return coord_lines, fold_lines


def fold_coord(coord: Coord, fold: Fold) -> Coord:
    x, y = coord
    axis, pivot = fold
    if axis == 'y':
        if y > pivot:
            return x, pivot * 2 - y
        return x, y
    if axis == 'x':
        if x > pivot:
            return pivot * 2 - x, y
        return x, y


def part1(name: str):
    coords, folds = get_hashes_and_folds(name)
    first_fold = folds[0]
    print(len({fold_coord(coord, first_fold) for coord in coords}))


def part2(name: str):
    coords, folds = get_hashes_and_folds(name)
    all_folds = coords
    for fold in folds:
        all_folds = {fold_coord(coord, fold) for coord in all_folds}
    print_coords(all_folds)


def __test():
    part1('test')
    part2('test')


def __main():
    part1('input')
    part2('input')


if __name__ == '__main__':
    __test()
    __main()


