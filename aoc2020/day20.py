import math
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'


@dataclass
class Tile:
    char_grid: List[str]

    def top(self) -> str:
        return self.char_grid[0]

    def bottom(self) -> str:
        return self.char_grid[-1]

    def left(self) -> str:
        return ''.join(s[0] for s in self.char_grid)

    def right(self) -> str:
        return ''.join(s[-1] for s in self.char_grid)

    def v_flip(self):
        self.char_grid.reverse()

    def rotate_90(self):
        new_grid = defaultdict(dict)
        for y in range(0, len(self.char_grid)):
            for x in range(0, len(self.char_grid[0])):
                new_grid[x][y] = self.char_grid[y][x]
        self.char_grid = [''.join(v.values())[::-1] for v in new_grid.values()]

    def print(self):
        for r in self.char_grid:
            print(r)


@dataclass
class TileGrid:
    id_to_tile: Dict[int, Tile]
    grid_to_unused: Optional[Dict[Tuple[int, ...], Tuple[int, ...]]] = None

    @property
    def side_len(self) -> int:
        return int(math.sqrt(len(self.id_to_tile)))

    def get_corners(self) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        return (0, 0), (self.side_len - 1, 0), (0, self.side_len - 1), (self.side_len - 1, self.side_len - 1)

    def get_neighbors(self, pos: Tuple[int, int], grid: Dict[Tuple[int, int], int]) -> Tuple[
        Optional[Tile], Optional[Tile],
        Optional[Tile], Optional[Tile]]:
        x, y = pos
        up = self.id_to_tile.get(grid.get((x, y - 1)))
        down = self.id_to_tile.get(grid.get((x, y + 1)))
        left = self.id_to_tile.get(grid.get((x - 1, y)))
        right = self.id_to_tile.get(grid.get((x + 1, y)))
        return up, down, left, right

    def add_tile_at(self, tile_id: int, pos: Tuple[int, int], grid: Dict[Tuple[int, int], int]) -> bool:
        tile = self.id_to_tile[tile_id]
        up, down, left, right = self.get_neighbors(pos, grid)

        def match(t: Tile, n: Optional[Tile], d: int):
            if n is None:
                return True
            t_edges = [t.top(), t.bottom(), t.left(), t.right()]
            match_edges = [n.bottom(), n.top(), n.right(), n.left()]
            return t_edges[d] == match_edges[d]

        def fits():
            return match(tile, up, 0) and match(tile, down, 1) and match(tile, left, 3) and match(tile, right, 4)

        flips = 0
        while flips < 2:
            rotates = 0
            while rotates < 4:
                if fits():
                    return True
                tile.rotate_90()
                rotates += 1
            tile.v_flip()
            flips += 1
        return False

    def fill_next(self, grid: Dict[Tuple[int, int], int], next_pos: Tuple[int, int], unused_ids: Set[int]) -> int:
        for tile_id in unused_ids:
            if self.add_tile_at(tile_id, next_pos, grid):
                return tile_id
        return -1

    def fill_all(self) -> Dict[Tuple[int, int], int]:
        self.grid_to_unused = {}

        def advance(np: Tuple[int, int]) -> Tuple[int, int]:
            x, y = np
            x = x + 1
            if x >= self.side_len:
                x = 0
                y = y + 1
            return x, y

        def retreat(np: Tuple[int, int]) -> Tuple[int, int]:
            x, y = np
            x = x - 1
            if x < 0:
                x = self.side_len - 1
                y = y - 1
            if x == 0 and y == 0:
                raise Exception('Should not retreat this far...')
            return x, y

        def attempt_fill(g: Dict[Tuple[int, int], int], npos: Tuple[int, int],
                         remain_ids: Set[int]) -> Optional[Dict[Tuple[int, int], int]]:
            while True:
                next_id = self.fill_next(g, npos, remain_ids)
                if next_id != -1:
                    g[npos] = next_id
                    remain_ids.remove(next_id)
                    grid_hash = tuple(g.values())
                    self.grid_to_unused[grid_hash] = tuple(remain_ids)
                    if npos == (self.side_len - 1, self.side_len - 1):
                        return g
                    npos = advance(npos)
                else:
                    grid_hash = tuple(g.values())
                    remain_ids = set(self.grid_to_unused[grid_hash])
                    try:
                        npos = retreat(npos)
                    except Exception as e:
                        return None

        for tile_id, tile in self.id_to_tile.items():
            flips = 0
            while flips < 2:
                rotations = 0
                while rotations < 4:
                    next_pos = 0, 0
                    grid = {next_pos: tile_id}
                    grid_hash = tuple(grid.values())
                    unused_ids = set(self.id_to_tile.keys()) - {tile_id}
                    self.grid_to_unused[grid_hash] = tuple(unused_ids)
                    fin_grid = attempt_fill(grid, advance(next_pos), unused_ids)
                    if fin_grid is not None:
                        return fin_grid
                    tile.rotate_90()
                    rotations += 1
                tile.v_flip()
                flips += 1
        raise Exception('No configuration found')


def part1(in_file: List[str]):
    tiles = [i.split('\n') for i in in_file]
    tile_map = {}
    for tile in tiles:
        _, tile_id = tile[0].split(' ')
        tile_map[int(tile_id[:-1])] = Tile(tile[1:])
    tg = TileGrid(tile_map)
    grid = tg.fill_all()
    tl, tr, bl, br = tg.get_corners()
    print(grid[tl] * grid[tr] * grid[bl] * grid[br])


def _run_program(input_path: str):
    in_file = U.read_chunked_lines(input_path)
    part1(in_file)


def __test():
    _run_program(f'{DATA_DIR}test')


def __main():
    _run_program(f'{DATA_DIR}day20')


if __name__ == '__main__':
    # __test()
    __main()
