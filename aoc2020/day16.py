from collections import defaultdict, deque
from functools import reduce
from operator import mul

from dataclasses import dataclass

import utils as U
from typing import List, Tuple

DATA_DIR = './inputs/'


def get_parts(path: str) -> Tuple[List[str], str, List[str]]:
    rules, my_ticket, other_tickets = tuple(U.read_chunked_lines(path))
    rules = rules.split('\n')
    _, my_ticket = tuple(my_ticket.split('\n'))
    other_tickets = other_tickets.split('\n')[1:]
    return rules, my_ticket, other_tickets


@dataclass
class Rule:
    field: str
    range1: range
    range2: range

    @classmethod
    def from_str(cls, s: str) -> 'Rule':
        field, ranges = tuple(s.split(': '))
        r1, r2 = tuple(ranges.split(' or '))
        range1_start, range1_end = tuple(r1.split('-'))
        range2_start, range2_end = tuple(r2.split('-'))
        return cls(field, range(int(range1_start), int(range1_end) + 1), range(int(range2_start), int(range2_end) + 1))

    def is_valid(self, num: int) -> bool:
        return num in self.range1 or num in self.range2

    def __eq__(self, other):
        return self.field == other.field and self.range1 == other.range1 and self.range2 == other.range2

    def __hash__(self):
        return self.field.__hash__()


def part1(rules: List[str], nearby_tickets: List[str]) -> List[str]:
    valid_tickets = set(nearby_tickets)
    error_rate = 0
    rules = list(map(Rule.from_str, rules))
    for t in nearby_tickets:
        field_vals = (int(v) for v in t.split(','))
        for val in field_vals:
            if not any(r.is_valid(val) for r in rules):
                error_rate += val
                valid_tickets.remove(t)
    print(error_rate)
    return list(valid_tickets)


def part2(rules: List[str], my_ticket: str, valid_tickets: List[str]):
    my_ticket = list(map(int, my_ticket.split(',')))
    final_ticket = {}
    rules = set(map(Rule.from_str, rules))
    valid_tickets = [list(map(int, t.split(','))) for t in valid_tickets]
    unknown_fields = deque(range(0, len(my_ticket)))
    while len(unknown_fields) > 0:
        i = unknown_fields.popleft()
        candidates = []
        valid_values = {t[i] for t in valid_tickets}
        for r in rules:
            if all(r.is_valid(v) for v in valid_values):
                print(f'slot {i} could be {r.field}')
                candidates.append(r)
        if len(candidates) == 1:
            rule = candidates[0]
            print(f'slot {i} is {rule.field}')
            rules.remove(rule)
            final_ticket[rule.field] = my_ticket[i]
        else:
            unknown_fields.append(i)
    print(final_ticket)
    departures = {k: v for k, v in final_ticket.items() if 'departure' in k}
    print(departures)
    mults = {v for k, v in departures.items()}
    print(mults)
    print(reduce(mul, mults))


def __test():
    rules, my_ticket, other_tickets = get_parts(f'{DATA_DIR}test')
    valid_tickets = part1(rules, other_tickets)
    part2(rules, my_ticket, valid_tickets)


def __main():
    rules, my_ticket, other_tickets = get_parts(f'{DATA_DIR}day16')
    valid_tickets = part1(rules, other_tickets)
    part2(rules, my_ticket, valid_tickets)


if __name__ == '__main__':
    # __test()
    __main()
