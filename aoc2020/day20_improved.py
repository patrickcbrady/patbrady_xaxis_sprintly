import math
from functools import lru_cache
from typing import List, Dict, Tuple, Optional, Set

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'


@lru_cache()
def get_grid(char_grid: Tuple[str, ...], rotations: int, flipped: bool) -> List[str]:
    res = list(char_grid)
    if flipped:
        res = res[::-1]
    if rotations == 1:
        res = [''.join(t) for t in zip(*res[::-1])]
    elif rotations == 2:
        res = [s[::-1] for s in res[::-1]]
    elif rotations == 3:
        res = [''.join(t) for t in list(zip(*res))[::-1]]
    return res


class Tile:
    def __init__(self, char_grid: List[str]):
        self.char_grid = char_grid
        self.edges = self._init_edges(char_grid)
        self.flipped = False
        self.rotations = 0

    @staticmethod
    def _init_edges(char_grid: List[str]) -> List[str]:
        """return a list of the tile's edges in top, right, bottom, left order"""
        return [char_grid[0], ''.join(s[-1] for s in char_grid), char_grid[-1], ''.join(s[0] for s in char_grid)]

    @property
    def top(self) -> str:
        return self.get_edge(0)

    @property
    def right(self) -> str:
        return self.get_edge(1)

    @property
    def bottom(self) -> str:
        return self.get_edge(2)

    @property
    def left(self) -> str:
        return self.get_edge(3)

    def get_edge(self, edge_idx: int) -> str:
        """
        return an edge string in top, right, bottom, left order by index 0-3,
        the edge string should be presented in top to bottom, left to right order
        """
        edges = self.edges
        if self.flipped:
            edges = [edges[2], edges[1], edges[0], edges[3]]
        rotation_idx = (edge_idx - self.rotations) % 4
        res = edges[rotation_idx]
        if (self.rotations == 1 and rotation_idx in (1, 3)) or self.rotations == 2 or (self.rotations == 3
                                                                                       and rotation_idx in (0, 2)):
            res = res[::-1]
        if self.flipped and rotation_idx in (1, 3):
            return res[::-1]
        return res

    def flip(self):
        self.flipped = not self.flipped

    def rotate_90(self):
        self.rotations = (self.rotations + 1) % 4

    @property
    def grid(self) -> List[str]:
        return get_grid(tuple(self.char_grid), self.rotations, self.flipped)

    @grid.setter
    def grid(self, grid: List[str]):
        res = grid
        if self.flipped:
            res = res[::-1]
        if self.rotations == 1:
            res = [''.join(t) for t in list(zip(*res))[::-1]]
        elif self.rotations == 2:
            res = [s[::-1] for s in res[::-1]]
        elif self.rotations == 3:
            res = [''.join(t) for t in zip(*res[::-1])]
        self.char_grid = res

    def print(self):
        for r in self.grid:
            print(r)

    def match_top_and_left(self, top: Optional['Tile'] = None, left: Optional['Tile'] = None) -> bool:
        """
        return True if this tile is oriented such that its top and left edges match the bottom and right edges of
        tiles 'top' and 'left'. If all orientations are exhausted with no match, return False
        """
        flips = 0
        while flips < 2:
            rotates = 0
            while rotates < 4:
                if (top is None or self.top == top.bottom) and (left is None or self.left == left.right):
                    return True
                else:
                    self.rotate_90()
                    rotates += 1
            self.flip()
            flips += 1
        return False


@dataclass
class TileGrid:
    id_to_tile: Dict[int, Tile]
    grid_to_unused: Optional[Dict[Tuple[int, ...], Tuple[int, ...]]] = None
    filled_grid = None

    @property
    def side_len(self) -> int:
        return int(math.sqrt(len(self.id_to_tile)))

    def get_corners(self) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        return (0, 0), (self.side_len - 1, 0), (0, self.side_len - 1), (self.side_len - 1, self.side_len - 1)

    def get_top_left(self, pos: Tuple[int, int], grid: Dict[Tuple[int, int], int]) -> Tuple[
        Optional[Tile], Optional[Tile]]:
        x, y = pos
        up = self.id_to_tile.get(grid.get((x, y - 1)))
        left = self.id_to_tile.get(grid.get((x - 1, y)))
        return up, left

    def add_tile_at(self, tile_id: int, pos: Tuple[int, int], grid: Dict[Tuple[int, int], int]) -> bool:
        tile = self.id_to_tile[tile_id]
        up, left = self.get_top_left(pos, grid)
        return tile.match_top_and_left(up, left)

    def fill_next(self, grid: Dict[Tuple[int, int], int], next_pos: Tuple[int, int], unused_ids: Set[int]) -> int:
        for tile_id in unused_ids:
            if self.add_tile_at(tile_id, next_pos, grid):
                return tile_id
        return -1

    def fill_all(self):
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
                    try:
                        grid_hash = tuple(g.values())
                        remain_ids = set(self.grid_to_unused[grid_hash])
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
                        self.filled_grid = fin_grid
                        return
                    tile.rotate_90()
                    rotations += 1
                tile.flip()
                flips += 1
        raise Exception('No configuration found')


def part1(in_file: List[str]) -> TileGrid:
    tiles = [i.split('\n') for i in in_file]
    tile_map = {}
    for tile in tiles:
        _, tile_id = tile[0].split(' ')
        tile_map[int(tile_id[:-1])] = Tile(tile[1:])
    tg = TileGrid(tile_map)
    with U.localtimer():
        tg.fill_all()
    grid = tg.filled_grid
    tl, tr, bl, br = tg.get_corners()
    print(grid[tl] * grid[tr] * grid[bl] * grid[br])
    return tg


def get_image(t: Tile) -> List[str]:
    return [s[1:-1] for s in t.grid[1:-1]]


def is_sea_monster(row_1, row_2, row_3):
    res = True
    row_1_slots = {18}
    row_2_slots = {0, 5, 6, 11, 12, 17, 18, 19}
    row_3_slots = {1, 4, 7, 10, 13, 16}
    for slot in row_1_slots:
        res = res and row_1[slot] == '#'
    for slot in row_2_slots:
        res = res and row_2[slot] == '#'
    for slot in row_3_slots:
        res = res and row_3[slot] == '#'
    return res


def count_monsters(big_tile: Tile) -> int:
    sea_monster_len = 20
    sea_monster_count = 0
    sea_monster_tops = []
    for row in range(0, len(big_tile.grid) - 2):
        full_rows = tuple(big_tile.grid[row:row + 3])
        i = 0
        while i < len(full_rows[0]) - sea_monster_len:
            row_1, row_2, row_3 = tuple(r[i: i + sea_monster_len] for r in full_rows)
            if is_sea_monster(row_1, row_2, row_3):
                sea_monster_count += 1
                sea_monster_tops.append((row, i + 18))
            i += 1
    for row_idx, head_pos in sea_monster_tops:
        row = big_tile.grid[row_idx]
        big_tile.grid[row_idx] = row[0:head_pos] + 'O' + row[head_pos + 1:]
        row = big_tile.grid[row_idx + 1]
        big_tile.grid[row_idx + 1] = row[0:head_pos - 18] + 'O' + row[head_pos - 17:head_pos - 13] + 'OO' + row[
                                                                                                            head_pos - 11: head_pos - 7] + 'OO' + row[
                                                                                                                                                  head_pos - 5: head_pos - 1] + 'OOO' + row[
                                                                                                                                                                                        head_pos + 2:]
        row = big_tile.grid[row_idx + 2]
        big_tile.grid[row_idx + 2] = row[0:head_pos - 17] + 'O' + row[head_pos - 16:head_pos - 14] + 'O' + row[
                                                                                                           head_pos - 13:head_pos - 11] + 'O' + row[
                                                                                                                                                head_pos - 10:head_pos - 8] + 'O' + row[
                                                                                                                                                                                    head_pos - 7:head_pos - 5] + 'O' + row[
                                                                                                                                                                                                                       head_pos - 4:head_pos - 2] + 'O' + row[
                                                                                                                                                                                                                                                          head_pos - 1:]
    return sea_monster_count


def print_results(big_map: Tile):
    big_map.print()
    print(f'water choppiness is {sum(s.count("#") for s in big_map.grid)}')


def print_tile_grid(tg: TileGrid):
    for y in range(0, tg.side_len):
        tile_ids = [str(tg.filled_grid[(x, y)]) for x in range(0, tg.side_len)]
        print(' '.join(tile_ids))
        print('\n')

    sample_tile = tg.id_to_tile[tg.filled_grid[(0, 0)]]
    for y in range(0, tg.side_len):
        tiles = [tg.id_to_tile[tg.filled_grid[(x, y)]] for x in range(0, tg.side_len)]
        for i in range(0, len(sample_tile.grid)):
            print(' '.join(t.grid[i] for t in tiles))
        print('\n')
    print('\n')


def part2(tg: TileGrid):
    image_grid = {}
    print('== Grid Info ==')
    print(f'the grid is a square of {tg.side_len} x {tg.side_len} tiles')
    sample_tile = tg.id_to_tile[tg.filled_grid[(0, 0)]]
    print(f'each tile is {len(sample_tile.grid[0])} x {len(sample_tile.grid)}')
    for pos, tile_id in tg.filled_grid.items():
        tile = tg.id_to_tile[tile_id]
        image_grid[pos] = get_image(tile)
    sample_img = image_grid[(0, 0)]
    print(f'after stripping the edges, the new tiles are {len(sample_img[0])} x {len(sample_img)}')
    big_tile_grid = []
    for y in range(0, tg.side_len):
        row_tiles = [image_grid[(x, y)] for x in range(0, tg.side_len)]
        tile_height = len(row_tiles[0])
        for row in range(0, tile_height):
            big_tile_grid.append(''.join(t[row] for t in row_tiles))
    big_map = Tile(big_tile_grid)
    print(
        f'After stitching the new tiles into a big tile, the big tile is {len(big_map.grid[0])} x {len(big_map.grid)}')
    flips = 0
    while flips < 2:
        rotates = 0
        while rotates < 4:
            sea_monsters = count_monsters(big_map)
            print(f'After {flips} flips and {rotates} rotations, we find {sea_monsters} sea monsters')
            if sea_monsters > 0:
                print_results(big_map)
                return
            big_map.rotate_90()
            rotates += 1
        big_map.flip()
        flips += 1
    raise Exception('No sea monsters found')


def _run_program(input_path: str):
    in_file = U.read_chunked_lines(input_path)
    tg = part1(in_file)
    part2(tg)


def __test():
    _run_program(f'{DATA_DIR}test')


def __main():
    _run_program(f'{DATA_DIR}day20')


if __name__ == '__main__':
    # __test()
    __main()
