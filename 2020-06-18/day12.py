from typing import List, Union, Callable, Dict

from utils import read_path_lines, localtimer

DATA_DIR = './'


class Program:
    def __init__(self, instructions: List[str], registers: Dict[str, int]):
        self.instructions = instructions
        self.registers = registers

    def run(self):
        index = 0
        while index < len(self.instructions):
            index += self.execute(self.instructions[index])
        print(self.registers)

    def execute(self, instruction: str) -> int:
        parts = instruction.split(' ')
        cmd = parts[0]
        return self.commands[cmd](*parts[1:])

    @property
    def commands(self) -> Dict[str, Callable]:
        return {'cpy': self.copy,
                'inc': self.inc,
                'dec': self.dec,
                'jnz': self.jnz}

    def copy(self, val: str, register: str) -> int:
        val_to_copy = self.registers.get(val)
        if val_to_copy is None:
            val_to_copy = int(val)
        self.registers[register] = val_to_copy
        return 1

    def inc(self, register: str) -> int:
        self.registers[register] += 1
        return 1

    def dec(self, register: str) -> int:
        self.registers[register] -= 1
        return 1

    def jnz(self, val: str, amt: str) -> int:
        if val == '0' or self.registers.get(val) == 0:
            return 1
        return int(amt)


def __main():
    input = read_path_lines(f'{DATA_DIR}input')

    with localtimer():
        print('Part 1')
        Program(input, dict(a=0, b=0, c=0, d=0)).run()

    with localtimer():
        print('Part 2')
        Program(input, dict(a=0, b=0, c=1, d=0)).run()


if __name__ == '__main__':
    __main()
