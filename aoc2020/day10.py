from collections import defaultdict
from typing import List

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'


@dataclass
class AdapterChain:
    nodes: List[int]

    def connect_all(self) -> int:
        one_jolt_diffs = 0
        three_jolt_diffs = 0
        joltage = 0
        for j in sorted(self.nodes):
            diff = j - joltage
            if diff == 1:
                one_jolt_diffs += 1
            if diff == 3:
                three_jolt_diffs += 1
            joltage = j
        three_jolt_diffs += 1
        return one_jolt_diffs * three_jolt_diffs

    def count_all_paths(self):
        nodes = sorted(self.nodes)
        nodes = [0, *nodes, nodes[-1] + 3]
        nums = set(nodes)
        paths = defaultdict(int)
        for n in nodes:
            if n == 0:
                paths[n] = 1
            else:
                # no. of paths to current node is sum of no. of paths to the nodes that can reach the current node
                for m in range(n-3, n):
                    if m in nums:
                        paths[n] += paths[m]
        return paths[nodes[-1]]


def part1(a: AdapterChain):
    print(a.connect_all())


def part2(a: AdapterChain):
    print(a.count_all_paths())


def __main():
    adapters = AdapterChain(list(map(int, U.read_path_lines(f'{DATA_DIR}day10'))))
    part1(adapters)
    part2(adapters)


if __name__ == '__main__':
    __main()
