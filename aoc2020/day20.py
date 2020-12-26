import math
import pickle
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set, Generator

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
    filled_grid = None

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
                        self.filled_grid = fin_grid
                        return
                    tile.rotate_90()
                    rotations += 1
                tile.v_flip()
                flips += 1
        raise Exception('No configuration found')


def part1(in_file: List[str]) -> TileGrid:
    try:
        with open('./day20_part2_input.p', 'rb') as f:
            tg = pickle.load(f)
    except FileNotFoundError:
        tiles = [i.split('\n') for i in in_file]
        tile_map = {}
        for tile in tiles:
            _, tile_id = tile[0].split(' ')
            tile_map[int(tile_id[:-1])] = Tile(tile[1:])
        tg = TileGrid(tile_map)
        tg.fill_all()
        with open('./day20_part2_input.p', 'wb') as f:
            pickle.dump(tg, f)
    grid = tg.filled_grid
    tl, tr, bl, br = tg.get_corners()
    print(grid[tl] * grid[tr] * grid[bl] * grid[br])
    return tg


def get_image(t: Tile) -> List[str]:
    return [s[1:-1] for s in t.char_grid[1:-1]]


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
    for row in range(0, len(big_tile.char_grid) - 2):
        full_rows = tuple(big_tile.char_grid[row:row + 3])
        i = 0
        while i < len(full_rows[0]) - sea_monster_len:
            row_1, row_2, row_3 = tuple(r[i: i + sea_monster_len] for r in full_rows)
            if is_sea_monster(row_1, row_2, row_3):
                sea_monster_count += 1
                sea_monster_tops.append((row, i + 18))
            i += 1
    for row_idx, head_pos in sea_monster_tops:
        row = big_tile.char_grid[row_idx]
        big_tile.char_grid[row_idx] = row[0:head_pos] + 'O' + row[head_pos + 1:]
        row = big_tile.char_grid[row_idx + 1]
        big_tile.char_grid[row_idx + 1] = row[0:head_pos - 18] + 'O' + row[head_pos - 17:head_pos - 13] + 'OO' + row[
                                                                                                                 head_pos - 11: head_pos - 7] + 'OO' + row[
                                                                                                                                                       head_pos - 5: head_pos - 1] + 'OOO' + row[
                                                                                                                                                                                             head_pos + 2:]
        row = big_tile.char_grid[row_idx + 2]
        big_tile.char_grid[row_idx + 2] = row[0:head_pos - 17] + 'O' + row[head_pos - 16:head_pos - 14] + 'O' + row[
                                                                                                                head_pos - 13:head_pos - 11] + 'O' + row[
                                                                                                                                                     head_pos - 10:head_pos - 8] + 'O' + row[
                                                                                                                                                                                         head_pos - 7:head_pos - 5] + 'O' + row[
                                                                                                                                                                                                                            head_pos - 4:head_pos - 2] + 'O' + row[
                                                                                                                                                                                                                                                               head_pos - 1:]
    return sea_monster_count


def print_results(big_map: Tile):
    # big_map.print()
    print(f'water choppiness is {sum(s.count("#") for s in big_map.char_grid)}')


def print_tile_grid(tg: TileGrid):
    for y in range(0, tg.side_len):
        tile_ids = [str(tg.filled_grid[(x, y)]) for x in range(0, tg.side_len)]
        print(' '.join(tile_ids))
        print('\n')

    sample_tile = tg.id_to_tile[tg.filled_grid[(0, 0)]]
    for y in range(0, tg.side_len):
        tiles = [tg.id_to_tile[tg.filled_grid[(x, y)]] for x in range(0, tg.side_len)]
        for i in range(0, len(sample_tile.char_grid)):
            print(' '.join(t.char_grid[i] for t in tiles))
        print('\n')
    print('\n')


def ensure_fit(tg: TileGrid):
    """orient the tiles in a filled TileGrid so that they are all aligned"""

    def up_fits(tile, up) -> bool:
        return up is None or tile.top() == up.bottom()

    def down_fits(tile, down) -> bool:
        return down is None or tile.bottom() == down.top()

    def left_fits(tile, left) -> bool:
        return left is None or tile.left() == left.right()

    def right_fits(tile, right) -> bool:
        return right is None or tile.right() == right.left()

    def spin_flipper(t: Tile) -> Generator:
        flips = 0
        while flips < 2:
            rotates = 0
            while rotates < 4:
                t.rotate_90()
                yield t
                rotates += 1
            t.v_flip()
            yield t
            flips += 1

    def make_top_left_fit() -> bool:
        top_left = tg.id_to_tile[tg.filled_grid[(0, 0)]]
        right = tg.id_to_tile[tg.filled_grid[(1, 0)]]
        down = tg.id_to_tile[tg.filled_grid[(0, 1)]]
        tl_o = spin_flipper(top_left)
        r_o = spin_flipper(right)
        d_o = spin_flipper(down)

        if right_fits(top_left, right) and down_fits(top_left, down):
            return True

        for tl in tl_o:
            for r in r_o:
                for d in d_o:
                    if right_fits(tl, r) and down_fits(tl, d):
                        return True
                d_o = spin_flipper(down)
            r_o = spin_flipper(right)
        return False

    make_top_left_fit()

    def make_fit_up_and_left(tile, up, left) -> bool:
        t_o = spin_flipper(tile)
        if up_fits(tile, up) and left_fits(tile, left):
            return True
        for t in t_o:
            if up_fits(tile, up) and left_fits(tile, left):
                return True
        return False

    locked_positions = {(0, 0), (1, 0), (0, 1)}
    for y in range(0, tg.side_len):
        for x in range(0, tg.side_len):
            if (x, y) in locked_positions:
                continue
            up_pos, left_pos = (x, y - 1), (x - 1, y)
            tile_id = tg.filled_grid[(x, y)]
            up_id = tg.filled_grid[up_pos] if y > 0 else None
            left_id = tg.filled_grid[left_pos] if x > 0 else None
            tile, up, left = tuple(tg.id_to_tile[tid] if tid is not None else None for tid in (tile_id, up_id, left_id))
            res = make_fit_up_and_left(tile, up, left)
            locked_positions.add((x, y))
            if not res:
                raise Exception('couldn\'t make it fit!')


def part2(tg: TileGrid):
    image_grid = {}
    ensure_fit(tg)
    print('== Grid Info ==')
    print(f'the grid is a square of {tg.side_len} x {tg.side_len} tiles')
    sample_tile = tg.id_to_tile[tg.filled_grid[(0, 0)]]
    print(f'each tile is {len(sample_tile.char_grid[0])} x {len(sample_tile.char_grid)}')
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
        f'After stitching the new tiles into a big tile, the big tile is {len(big_map.char_grid[0])} x {len(big_map.char_grid)}')
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
        big_map.v_flip()
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
