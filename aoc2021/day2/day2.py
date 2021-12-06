from typing import List

from utils import get_arg_list


class Submarine:
    def __init__(self):
        self.depth = 0
        self.pos = 0

    def forward(self, amt: int):
        self.pos += amt

    def down(self, amt: int):
        self.depth += amt

    def up(self, amt: int):
        self.depth -= amt

    def process_cmds(self, cmds: List[List[str]]):
        for cmd in cmds:
            func, amt = tuple(cmd)
            exec(f'self.{func}({amt})')

    def print(self):
        print(f'position: {self.pos}\ndepth: {self.depth}\nres: {self.pos * self.depth}')


class AimedSub(Submarine):
    def __init__(self):
        super().__init__()
        self.aim = 0

    def forward(self, amt: int):
        super().forward(amt)
        self.depth += amt * self.aim

    def down(self, amt: int):
        self.aim += amt

    def up(self, amt: int):
        self.aim -= amt


def run(input_file: str):
    cmds = get_arg_list(input_file)
    sub = Submarine()
    sub.process_cmds(cmds)
    sub.print()
    sub2 = AimedSub()
    sub2.process_cmds(cmds)
    sub2.print()


def __test():
    run('test')


def __main():
    run('input')


if __name__ == '__main__':
    __test()
    __main()
