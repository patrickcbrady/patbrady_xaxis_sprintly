from typing import List

import utils as U

DATA_DIR = './inputs/'


def speaking_game(nums: List[int], game_end: int):
    with U.localtimer():
        num_to_turn = {n: i + 1 for i, n in enumerate(nums)}
        prev_num = 0
        prev_turn = len(nums) + 1
        while prev_turn < game_end:
            num_was_spoken = num_to_turn.get(prev_num, 0) != 0
            if num_was_spoken:
                spoken_num = prev_turn - num_to_turn[prev_num]
            else:
                spoken_num = 0
            num_to_turn[prev_num] = prev_turn
            prev_turn += 1
            prev_num = spoken_num
    print(prev_num)


def part1(nums: List[int]):
    speaking_game(nums, 2020)


def part2(nums: List[int]):
    speaking_game(nums, 30000000)


def __test():
    nums = [int(n) for n in U.read_path_csv(f'{DATA_DIR}test')]
    part1(nums)
    part2(nums)


def __main():
    nums = [int(n) for n in U.read_path_csv(f'{DATA_DIR}day15')]
    part1(nums)
    part2(nums)


if __name__ == '__main__':
    # __test()
    __main()
