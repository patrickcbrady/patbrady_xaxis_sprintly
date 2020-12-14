import re
from collections import defaultdict
from typing import List

import utils as U

DATA_DIR = './inputs/'


class Interpreter:
    def __init__(self):
        self.mem = defaultdict(int)
        self.and_mask = int('111111111111111111111111111111111111', base=2)
        self.or_mask = int('000000000000000000000000000000000000', base=2)

    def set_mask(self, bit_mask: str):
        self.and_mask = int(bit_mask.replace('X', '1'), base=2)
        self.or_mask = int(bit_mask.replace('X', '0'), base=2)
        # print(f'{self.and_mask:b}')
        # print(f'{self.or_mask:b}')

    def apply_mask(self, val: int) -> int:
        # print(f'{val:036b}')
        masked_val = val & self.and_mask | self.or_mask
        # print(f'{masked_val:036b}')
        return masked_val

    def set_addr(self, cmd: str, val: str):
        addr = int(cmd[cmd.index('[') + 1: cmd.index(']')])
        self.mem[addr] = self.apply_mask(int(val))

    def interpret(self, instruction: str):
        cmd, val = tuple(instruction.split(' = '))
        # print(cmd, val)
        if cmd == 'mask':
            self.set_mask(val)
        elif 'mem' in cmd:
            self.set_addr(cmd, val)

    def get_mem_sum(self) -> int:
        return sum(self.mem.values())


class InterpreterV2(Interpreter):
    def __init__(self):
        super().__init__()
        self.mask = '000000000000000000000000000000000000'

    def set_addr(self, cmd: str, val: str):
        addr = int(cmd[cmd.index('[') + 1: cmd.index(']')])
        float_masks = re.sub('[^X]', '', self.mask)
        d = len(float_masks)
        max_mask = int(re.sub('[X]', '1', float_masks), base=2)
        addr_str = f'{addr:036b}'
        mask_iter = iter(self.mask)

        def addr_repl(s):
            c = next(mask_iter)
            return c if c in {'1', 'X'} else s.group(0)

        masked_addr = re.sub('[10]', addr_repl, addr_str)

        for i in range(0, max_mask + 1):
            binary = f'{i:0{d}b}'
            digits = iter(binary)

            def cb(c):
                return next(digits)

            mask = re.sub('[X]', cb, masked_addr)
            write_to = int(mask, base=2)
            self.mem[write_to] = int(val)

    def set_mask(self, bit_mask: str):
        self.mask = bit_mask


def part1(lines: List[str]):
    interpreter = Interpreter()
    for line in lines:
        interpreter.interpret(line)
    print(interpreter.get_mem_sum())


def part2(lines: List[str]):
    interpreter = InterpreterV2()
    for line in lines:
        interpreter.interpret(line)
    print(interpreter.get_mem_sum())


def __test():
    lines = U.read_path_lines(f'{DATA_DIR}test')
    part1(lines)
    lines2 = ['mask = 000000000000000000000000000000X1001X',
              'mem[42] = 100',
              'mask = 00000000000000000000000000000000X0XX',
              'mem[26] = 1']
    part2(lines2)


def __main():
    lines = U.read_path_lines(f'{DATA_DIR}day14')
    part1(lines)
    part2(lines)


if __name__ == '__main__':
    # __test()
    __main()
