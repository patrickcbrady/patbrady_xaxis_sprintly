from typing import List, Dict


class BrokenClock:
    """It's right twice a day!"""

    NUM_TO_SEGS = {
        1: 2,
        4: 4,
        7: 3,
        8: 7
    }

    def __init__(self, patterns: List[List[str]], outputs: List[List[str]]):
        self.patterns = patterns
        self.outputs = outputs
        self.uniques_to_outputs = {k: [o for output in outputs for o in output if len(o) == l] for k, l in
                                   self.NUM_TO_SEGS.items()}

    @classmethod
    def from_file(cls, name: str):
        with open(f'./{name}') as f:
            lines = f.read().split('\n')
            patterns, outputs = zip(*[line.split(' | ') for line in lines])
            return cls([p.split(' ') for p in patterns], [o.split(' ') for o in outputs])

    def count_uniques(self):
        return sum(len(v) for v in self.uniques_to_outputs.values())

    @staticmethod
    def derive_numbers(pattern_set: List[str]) -> Dict[str, int]:
        len_to_pattern = {}
        for pattern in pattern_set:
            if len(pattern) in len_to_pattern:
                len_to_pattern[len(pattern)].add(pattern)
            else:
                len_to_pattern[len(pattern)] = {pattern}
        one = len_to_pattern[2].pop()
        two_three_five = len_to_pattern[5]
        four = len_to_pattern[4].pop()
        six_nine_zero = len_to_pattern[6]
        seven = len_to_pattern[3].pop()
        eight = len_to_pattern[7].pop()
        a = (set(seven) - set(one)).pop()
        three = {n for n in two_three_five if set(one).issubset(set(n))}.pop()
        b = (set(four) - set(three)).pop()
        five = {n for n in two_three_five if n != three and b in n}.pop()
        two = {n for n in two_three_five if n != three and n != five}.pop()
        f = (set(one) - set(two)).pop()
        c = (set(one) - set(five)).pop()
        six = {n for n in six_nine_zero if c not in set(n)}.pop()
        e = (set(six) - set(five)).pop()
        nine = {n for n in six_nine_zero if n != six and e not in set(n)}.pop()
        zero = {n for n in six_nine_zero if n != six and n != nine}.pop()
        d = (set(eight) - set(zero)).pop()
        g = (set(nine) - set(four) - {a}).pop()
        return {''.join(sorted(p)): i for i, p in
                enumerate((zero, one, two, three, four, five, six, seven, eight, nine))}

    def gen_outputs(self):
        total = 0
        for pattern_set, outputs in zip(self.patterns, self.outputs):
            p_to_n = self.derive_numbers(pattern_set)
            new_outputs = [p_to_n[''.join(sorted(o))] for o in outputs]
            total += int(''.join(map(str, new_outputs)))
        print(total)


def part1(name: str):
    print(BrokenClock.from_file(name).count_uniques())


def part2(name: str):
    BrokenClock.from_file(name).gen_outputs()


def __test():
    part1('large_test')
    part2('large_test')


def __main():
    part1('input')
    part2('input')


if __name__ == '__main__':
    __test()
    __main()
