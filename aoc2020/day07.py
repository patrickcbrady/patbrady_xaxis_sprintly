from functools import lru_cache
from typing import List, NamedTuple, Dict

import utils as U

DATA_DIR = './inputs/'


class BagContainer(NamedTuple):
    bags: Dict[str, Dict[str, int]] = {}

    @classmethod
    def from_bag_rules(cls, bag_rules: List[str]) -> 'BagContainer':
        res = cls()
        for r in bag_rules:
            res.read_bag_rule(r)
        return res

    def read_bag_rule(self, rule: str):
        container, contents = tuple(rule.split(' contain '))
        color = self.get_color_from_container_desc(container)
        self.bags[color] = {}
        if 'no other bags' in contents:
            return

        contents = contents.split(', ')
        for cd in contents:
            self.bags[color].update(self.get_dict_from_contents_desc(cd))

    @staticmethod
    def get_color_from_container_desc(container_desc: str) -> str:
        return container_desc[:container_desc.index(' bag')]

    @staticmethod
    def get_dict_from_contents_desc(contents_desc: str) -> Dict[str, int]:
        num, color_adj, color, _ = tuple(contents_desc.split(' '))
        return {f'{color_adj} {color}': int(num)}


def part1(bc: BagContainer):
    @lru_cache(maxsize=None)
    def can_contain(container_color: str, contents_color: str) -> bool:
        if bc.bags[container_color] == {}:
            return False
        if contents_color in set(bc.bags[container_color]):
            return True
        return any(can_contain(k, contents_color) for k in bc.bags[container_color])

    print(sum((1 for b in bc.bags.keys() if can_contain(b, 'shiny gold'))))


def part2(bc: BagContainer):
    @lru_cache(maxsize=None)
    def bag_total(container_color: str) -> int:
        if bc.bags[container_color] == {}:
            return 0
        else:
            return sum((v + (bag_total(k) * v) for k, v in bc.bags[container_color].items()))

    print(bag_total('shiny gold'))


def __main():
    bag_rules = U.read_path_lines(f'{DATA_DIR}day7')
    bc = BagContainer.from_bag_rules(bag_rules)
    part1(bc)
    part2(bc)


if __name__ == '__main__':
    __main()
