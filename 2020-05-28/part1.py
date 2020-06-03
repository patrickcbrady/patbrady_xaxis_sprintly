from functools import lru_cache
from typing import List, NamedTuple, Callable, Set

DATA_DIR = './'


class Comp(NamedTuple):
    port_a: int
    port_b: int

    @classmethod
    def from_str(cls, port_str: str):
        return cls(*map(int, port_str.split('/')))

    @property
    def strength(self):
        return sum(self)

    def other(self, port_size: int):
        return self.port_b if self.port_a == port_size else self.port_a

    def __hash__(self):
        return id(self)


class CompMap(dict):
    def __missing__(self, key):
        res = self[key] = set()
        return res

    def add(self, comp: Comp):
        self[comp.port_a].add(comp)
        self[comp.port_b].add(comp)


class BridgeInfo(NamedTuple):
    length: int
    strength: int


def read_file(filename: str) -> List[Comp]:
    data = open(f'{DATA_DIR}/{filename}', 'r').read().split('\n')
    return [Comp.from_str(d) for d in data]


def read_input_data() -> List[Comp]:
    return read_file('input')


def read_test_data() -> List[Comp]:
    return read_file('test-input')


def __main():
    comps = read_input_data()
    cmap = CompMap()
    for c in comps:
        cmap.add(c)

    @lru_cache(None)
    def _build_bridge(cur_port_size: int = 0, used_comps: Set[Comp] = frozenset(),
                      length: int = 0, key: Callable = lambda t: t[1]) -> BridgeInfo:
        available_comps = cmap[cur_port_size] - used_comps

        if not available_comps:
            return BridgeInfo(length, sum(c.strength for c in used_comps))

        res = [_build_bridge(c.other(cur_port_size), used_comps | {c}, length + 1, key) for c in available_comps]
        return max(res, key=key)

    print(f'part one: {_build_bridge()}')
    print(f'part two: {_build_bridge(key=lambda t: t)}')
    print(_build_bridge.cache_info())


if __name__ == '__main__':
    __main()
