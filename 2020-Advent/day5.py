from typing import Tuple, List

from utils import read_path_lines

DATA_DIR = './inputs/'


def fb_to_num(fb: str) -> int:
    return int(fb.replace('F', '0').replace('B', '1'), base=2)


def lr_to_num(lr: str) -> int:
    return int(lr.replace('R', '1').replace('L', '0'), base=2)


def parse_boarding_pass(bp: str) -> Tuple[int, int]:
    return fb_to_num(bp[0:7]), lr_to_num(bp[7:])


def get_seat_id(row: int, col: int) -> int:
    return row * 8 + col


def part1(bps: List[str]):
    print(max(get_seat_id(*parse_boarding_pass(bp)) for bp in bps))


def part2(bps: List[str]):
    ids = [get_seat_id(*parse_boarding_pass(bp)) for bp in bps]
    old_id = None
    for id in sorted(ids):
        if old_id:
            if id != 1 + old_id:
                print(f'Your seat ID should be {1 + old_id}')
                break
        old_id = id


def __main():
    boarding_passes = read_path_lines(f'{DATA_DIR}day5')
    # part1(boarding_passes)
    part2(boarding_passes)


if __name__ == '__main__':
    __main()
