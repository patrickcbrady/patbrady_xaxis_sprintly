from typing import Optional, Tuple, Set

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'


@dataclass
class Node:
    val: int
    next: Optional['Node'] = None

    def print(self):
        val_str = f'cups: ({self.val})'
        n = self.next
        while n != self and n is not None:
            val_str += f' {n.val}'
            n = n.next
        print(val_str)

    def __repr__(self):
        return f'Node({self.val}, {self.next.val})'


class CupsGame:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.current = None
        self.head = None
        self.tail = None
        self.item_map = {}
        self.select_num = 3
        self.move_count = 0
        self.min = 1
        self.max = 1

    def insert(self, val: int):
        if not self.current:
            self.current = Node(val)
            self.head = self.current
            self.tail = self.current
            self.current.next = self.current
        else:
            new_node = Node(val, self.head)
            self.tail.next = new_node
            self.tail = new_node

        self.item_map[val] = self.tail

    def inc_current(self):
        self.current = self.current.next

    def pick_up_cups(self) -> Tuple[Node, Node, Set[int]]:
        start_cup = self.current.next
        selected_vals = {start_cup.val}
        end_cup = start_cup
        for i in range(1, self.select_num):
            end_cup = end_cup.next
            selected_vals.add(end_cup.val)
        # excise and return the start and end of the picked-up cup chain
        self.current.next = end_cup.next
        end_cup.next = None
        return start_cup, end_cup, selected_vals

    def dec(self, d: int) -> int:
        if d - 1 < self.min:
            return self.max
        return d - 1

    def get_destination_cup(self, selected_vals: Set[int]) -> Node:
        destination = self.dec(self.current.val)
        while destination in selected_vals:
            destination = self.dec(destination)

        return self.item_map[destination]

    @staticmethod
    def place_cups(destination_cup: Node, start_cup: Node, end_cup: Node):
        new_end = destination_cup.next
        destination_cup.next = start_cup
        end_cup.next = new_end

    def log(self, msg: str):
        if self.debug:
            print(msg)

    def log_current(self):
        if self.debug:
            self.current.print()

    @staticmethod
    def get_str_from_node(node: Node) -> str:
        s = [f'{node.val}']
        n = node.next
        while n != node:
            s.append(f'{n.val}')
            n = n.next
        return ''.join(s)

    def log_state(self):
        if self.debug:
            s = ' '.join(self.get_str_from_node(self.head))
            curr = s.index(str(self.current.val))
            s = s[0:curr] + f'({s[curr]})' + s[curr + 1:]
            print(s)

    def play_move(self):
        self.move_count += 1
        # self.log(f'-- move {self.move_count} --')
        # self.log_state()
        start, end, pickup_vals = self.pick_up_cups()
        # self.log(f'pick up: {pickup_vals}')
        destination = self.get_destination_cup(pickup_vals)
        # self.log(f'destination: {destination.val}')
        self.place_cups(destination, start, end)
        self.inc_current()

    def _init_min_max(self):
        self.min = min(self.item_map)
        self.max = max(self.item_map)

    def do_moves(self, num_moves: int):
        self._init_min_max()
        with U.localtimer():
            for i in range(0, num_moves):
                self.play_move()
        self.log('-- final --')
        self.log_current()

    def print_from_1(self):
        one = self.item_map[1]
        print(self.get_str_from_node(one)[1:])


def part1(g: CupsGame):
    g.do_moves(100)
    g.print_from_1()


def part2(g: CupsGame):
    start_max = max(g.item_map) + 1
    with U.localtimer():
        for i in range(start_max, 1000000 + 1):
            g.insert(i)
    g.do_moves(10000000)
    one = g.item_map[1]
    print(one.next.val, one.next.next.val)
    print(one.next.val * one.next.next.val)


def _run_program(input_path):
    input_nums = U.read_whole_file(input_path)
    game = CupsGame(debug=False)
    for num in input_nums:
        game.insert(int(num))
    part1(game)
    game = CupsGame(debug=False)
    for num in input_nums:
        game.insert(int(num))
    part2(game)


def __test():
    _run_program(f'{DATA_DIR}test')


def __main():
    _run_program(f'{DATA_DIR}day23')


if __name__ == '__main__':
    # __test()
    __main()
