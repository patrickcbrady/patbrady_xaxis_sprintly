from collections import deque
from typing import List

from dataclasses import dataclass

import utils as U
from aoc2020.day1 import get_summands

DATA_DIR = './inputs/'


@dataclass
class XmasData:
    nums: List[int]
    preamble_len: int = 25

    def find_first_invalid(self):
        i = self.preamble_len
        try:
            while True:
                n = self.nums[i]
                preamble = self.nums[i - self.preamble_len:i]
                if get_summands(preamble, n) is None:
                    return n
                i += 1
        except IndexError:
            print('woops!')

    def exploit_weakness(self, weakness: int) -> int:
        """
        find the contiguous range in self.nums that sum to weakness
        return the sum of the smallest and largest numbers in that range
        """
        i = 0
        queue = deque()
        try:
            while True:
                queue.append(self.nums[i])
                while sum(queue) > weakness:
                    queue.popleft()
                if len(queue) > 1 and sum(queue) == weakness:
                    return max(queue) + min(queue)
                i += 1
        except IndexError:
            print('woops!')


def part1(xd: XmasData) -> int:
    return xd.find_first_invalid()


def part2(xd: XmasData, weakness: int) -> int:
    return xd.exploit_weakness(weakness)


def __main():
    data = list(map(int, U.read_path_lines(f'{DATA_DIR}day9')))
    xd = XmasData(data, 25)
    p1_res = part1(xd)
    print(p1_res)
    p2_res = part2(xd, p1_res)
    print(p2_res)


if __name__ == '__main__':
    __main()
