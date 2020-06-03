from typing import List, Dict
from abc import ABC, abstractmethod
import utils.core.utils as U

DATA_DIR = './'
DEBUG = False
OrbitMap = Dict[str, str]


def debug_log(msg: str):
    if DEBUG:
        print(msg)


def read_data(filename: str):
    data = open(f'{DATA_DIR}/{filename}', 'r').read().split('\n')
    return [str(x) for x in data]


class OrbitCounterBase(ABC):
    def __init__(self, file_name: str):
        text_map = read_data(file_name)
        self.orbit_map = self._parse_orbits(text_map)
        self.count_map = {}
        self._populate_count_map()

    @abstractmethod
    def _count_orbits(self, planet: str) -> int:
        pass

    @U.timer
    def _populate_count_map(self):
        for planet in self.orbit_map:
            self._count_orbits(planet)

    @staticmethod
    def _parse_orbits(text_map: List[str]) -> OrbitMap:
        return {row.split(')')[1]: row.split(')')[0] for row in text_map if ')' in row}

    def get_orbit_count(self):
        """return the total number of direct and indirect orbits based on the orbit map"""
        return sum(self.count_map.values())

    def get_min_orbits_to_santa(self):
        """
        return the minimum number of orbit jumps based on your map to get from the planet YOU are orbiting
        to the planet SAN is orbiting
        """
        # Get the cost in orbit jumps of getting from each of santa's indirect orbits to the planet santa is orbiting
        santa_cost_map = {}
        curr = self.orbit_map['SAN']
        cost = 0
        santa_to_com = set()
        while curr != 'COM':
            santa_to_com.add(curr)
            santa_cost_map[curr] = cost
            cost += 1
            curr = self.orbit_map[curr]

        # Find the first planet in your direct or indirect orbit that is also in santa's,
        # and return the cost of getting to that planet plus the cost of getting to santa from that planet
        curr = self.orbit_map['YOU']
        cost = 0
        while curr not in santa_to_com:
            cost += 1
            curr = self.orbit_map[curr]
        return cost + santa_cost_map[curr]


class OrbitCounterIter(OrbitCounterBase):
    def _count_orbits(self, planet: str) -> int:
        """return the count of orbits for a given planet, counting iteratively without memoization"""
        count = 0
        orig_planet = planet
        while planet != 'COM':
            count += 1
            planet = self.orbit_map[planet]
        self.count_map[orig_planet] = count
        return count


class OrbitCounterIterMemo(OrbitCounterBase):
    def _count_orbits(self, planet: str) -> int:
        """return the iteratively calculated count of orbits for a given planet, memoizing the result in count_map"""
        count, orig_planet = 0, planet
        while planet != 'COM':
            try:
                count += self.count_map[planet]
                break
            except KeyError:
                count += 1
                planet = self.orbit_map[planet]
        self.count_map[orig_planet] = count
        return count


class OrbitCounterRecursiveMemo(OrbitCounterBase):
    def _count_orbits(self, planet: str) -> int:
        """return the recursively calculated count of orbits for a given planet, memoizing the result in count_map"""
        if planet == 'COM':
            return 0
        try:
            return self.count_map[planet]
        except KeyError:
            self.count_map[planet] = 1 + self._count_orbits(self.orbit_map[planet])
            return self.count_map[planet]



def test_part_1():
    day_6_part_1_test = OrbitCounterRecursiveMemo('test')
    assert day_6_part_1_test.get_orbit_count() == 42


def test_part_2():
    day_6_part_2_test = OrbitCounterRecursiveMemo('test2')
    assert day_6_part_2_test.get_min_orbits_to_santa() == 4


def __main():
    test_part_1()
    test_part_2()
    day_6_puzzle = OrbitCounterRecursiveMemo('input')
    print(day_6_puzzle.get_orbit_count())
    print(day_6_puzzle.get_min_orbits_to_santa())
    print(f'Iterative approach: {OrbitCounterIter("input").get_orbit_count()}')
    print(f'Iterative with memoization: {OrbitCounterIterMemo("input").get_orbit_count()}')


if __name__ == '__main__':
    __main()
