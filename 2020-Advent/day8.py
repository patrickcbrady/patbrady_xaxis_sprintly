from dataclasses import dataclass

import utils as U
from typing import List, NamedTuple, Dict, Callable


DATA_DIR = './inputs/'


@dataclass
class GameConsole:
    instructions: List[str]
    accumulator: int = 0
    seen_indices = set()
    history = []
    fixes = 0

    def reset(self):
        self.accumulator = 0
        self.seen_indices = set()
        self.history = []

    @property
    def ops(self) -> Dict[str, Callable]:
        return {'nop': self.nop,
                'acc': self.acc,
                'jmp': self.jmp}

    def nop(self, val, index) -> int:
        return index + 1

    def acc(self, val, index) -> int:
        self.accumulator += val
        return index + 1

    def jmp(self, val, index) -> int:
        return index + val

    def run_instruction(self, index: int) -> int:
        if index in self.seen_indices:
            return -1
        self.history.append(index)
        self.seen_indices.add(index)
        instruction = self.instructions[index]
        op, val = tuple(instruction.split(' '))
        val = int(val)
        return self.ops[op](val, index)

    def run(self) -> int:
        index = 0
        while index != -1 and index < len(self.instructions):
            index = self.run_instruction(index)
        return index


def part1(gc: GameConsole):
    print('Part 1')
    gc.run()
    print(gc.accumulator)


def part2(gc: GameConsole):
    print('Part 2')
    i = gc.run()
    orig_instructions = gc.instructions
    orig_history = gc.history
    swap = {'jmp': 'nop', 'nop': 'jmp'}
    h = len(orig_history)
    while i == -1:
        gc.instructions = orig_instructions
        while True:
            h -= 1
            op, val = tuple(gc.instructions[orig_history[h]].split(' '))
            if op == 'jmp' or op == 'nop':
                op = swap[op]
                break
        gc.instructions[orig_history[h]] = ' '.join([op, val])
        gc.reset()
        i = gc.run()
    print(gc.accumulator)


def __main():
    instructions = U.read_path_lines(f'{DATA_DIR}day8')
    gc = GameConsole(instructions)
    part1(gc)
    gc.reset()
    part2(gc)


if __name__ == '__main__':
    __main()
