from typing import List, Set

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'


def _can_sum(pool: Set[int], target: int) -> bool:
    return any((target - p in pool) for p in pool if (target - p != p))


@dataclass
class XmasData:
    nums: List[int]
    preamble_len: int = 25

    def find_first_invalid(self):
        i = 0
        j = self.preamble_len
        preamble = set(self.nums[i:j])
        try:
            while True:
                n = self.nums[j]
                if not _can_sum(preamble, n):
                    return n
                preamble.remove(self.nums[i])
                i += 1
                preamble.add(self.nums[j])
                j += 1
        except IndexError:
            print('woops!')

    def exploit_weakness(self, weakness: int) -> int:
        """
        find the contiguous range in self.nums that sum to weakness
        return the sum of the smallest and largest numbers in that range
        """
        i = 0
        j = 1
        range_sum = self.nums[i] + self.nums[j]
        try:
            while range_sum != weakness:
                if range_sum < weakness:
                    j += 1
                    range_sum += self.nums[j]
                else:
                    range_sum -= self.nums[i]
                    i += 1
            cr = self.nums[i: j + 1]
            return min(cr) + max(cr)
        except IndexError:
            print('woops!')


def part1(xd: XmasData) -> int:
    return xd.find_first_invalid()


def part2(xd: XmasData, weakness: int) -> int:
    return xd.exploit_weakness(weakness)


def __main():
    data = list(map(int, U.read_path_lines(f'{DATA_DIR}day9')))
    xd = XmasData(data)
    p1_res = part1(xd)
    print(p1_res)
    p2_res = part2(xd, p1_res)
    print(p2_res)


if __name__ == '__main__':
    __main()
