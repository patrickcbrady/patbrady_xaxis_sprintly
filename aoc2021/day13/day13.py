from typing import List, Tuple

CoordList = List[Tuple[int, int]]
FoldList = List[Tuple[str, int]]


def get_hashes_and_folds(name: str) -> Tuple[CoordList, FoldList]:
    with open(f'./{name}') as f:
        lines = f.read().split('\n')
        break_point = lines.index('')
        coord_lines = [tuple(map(int, s.split(',')[:2])) for s in lines[:break_point]]
        fold_start = len('fold along ')
        fold_lines = [s[fold_start:].split('=') for s in lines[break_point + 1:]]
        fold_lines = list(map(lambda fold: (fold[0], int(fold[1])), fold_lines))
        return coord_lines, fold_lines

coords, folds = get_hashes_and_folds('test')
print(coords)