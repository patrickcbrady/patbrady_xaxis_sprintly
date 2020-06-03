from enum import Enum
from typing import List, Optional, Tuple, Union, Iterable, Iterator
from itertools import permutations

DATA_DIR = './'
DEBUG = False


def debug_log(msg: str):
    if DEBUG:
        print(msg)


def read_data(filename: str):
    data = open(f'{DATA_DIR}/{filename}', 'r').read().split(',')
    return [int(x) for x in data]


def init_day2_data():
    return read_data('input2')


def init_day5_data():
    return read_data('input5')


def init_day7_data():
    return read_data('input7')


class EndProgram(Exception):
    pass


class AwaitInput(Exception):
    pass


class OpsEnum(Enum):
        add = 1
        mult = 2
        save_input = 3
        print_output = 4
        jump_if_true = 5
        jump_if_false = 6
        less_than = 7
        equals = 8


class IntCodeComputer:
    def __init__(self, intcode: List[int], input_code: Optional[Union[Iterable[int], int]] = None):
        self.input = []
        if input_code is not None:
            input_code = input_code if isinstance(input_code, Iterable) else [input_code]
            self.input.extend(list(input_code))
        self.intcode = intcode
        self.pointer = 0
        self.output = None
        self.print_logs = True
        self.OPS = {
            1: (self.add, 3),
            2: (self.mult, 3),
            3: (self.save_input, 1),
            4: (self.print_output, 1),
            5: (self.jump_if_true, 2),
            6: (self.jump_if_false, 2),
            7: (self.less_than, 3),
            8: (self.equals, 3)
        }

    def reset(self, intcode: List[int]):
        self.intcode = intcode
        self.pointer = 0

    def mute(self):
        self.print_logs = False

    def log(self, msg):
        if self.print_logs:
            print(msg)

    def get_math_args(self, modes: List[int]) -> Tuple[int, int]:
        intcode = self.intcode
        a = intcode[self.pointer + 1] if modes[0] == 1 else intcode[intcode[self.pointer + 1]]
        b = intcode[self.pointer + 2] if modes[1] == 1 else intcode[intcode[self.pointer + 2]]
        return a, b

    def mult(self, modes: List[int]):
        operand, multiplicand = self.get_math_args(modes)
        res = operand * multiplicand
        output_idx = self.intcode[self.pointer + 3]
        self.intcode[output_idx] = res

    def add(self, modes: List[int]):
        res = sum(self.get_math_args(modes))
        output_idx = self.intcode[self.pointer + 3]
        self.intcode[output_idx] = res

    def save_input(self, modes: List[int]):
        save_idx = self.intcode[self.pointer + 1]
        try:
            self.intcode[save_idx] = self.input.pop(0)
        except IndexError:
            raise AwaitInput

    def print_output(self, modes: List[int]):
        output_idx = self.pointer + 1 if modes[0] == 1 else self.intcode[self.pointer + 1]
        self.output = self.intcode[output_idx]
        self.log(self.output)

    def jump_if_true(self, modes: List[int]) -> Optional[int]:
        jump_bool, jump_pos = self.get_math_args(modes)
        debug_log(f'jump_if_true: jump to {jump_pos} if {jump_bool} is not 0')
        if jump_bool != 0:
            return jump_pos

    def jump_if_false(self, modes: List[int]) -> Optional[int]:
        jump_bool, jump_pos = self.get_math_args(modes)
        debug_log(f'jump_if_false: jump to {jump_pos} if {jump_bool} is 0')
        if jump_bool == 0:
            return jump_pos

    def less_than(self, modes: List[int]):
        a, b = self.get_math_args(modes)
        output_idx = self.intcode[self.pointer + 3]
        self.intcode[output_idx] = 1 if a < b else 0

    def equals(self, modes: List[int]):
        a, b = self.get_math_args(modes)
        output_idx = self.intcode[self.pointer + 3]
        self.intcode[output_idx] = 1 if a == b else 0

    def run_instruction(self) -> int:
        opcode = int(str(self.intcode[self.pointer])[-2:])
        if opcode == 99:
            raise EndProgram()
        if opcode not in (self.OPS.keys() | {99}):
            raise Exception(f'opcode must be one of {list(self.OPS.keys() | {99})}')
        op_name = OpsEnum(opcode).name
        op, param_count = self.OPS[opcode]
        params = [self.intcode[self.pointer + x] for x in range(1, param_count + 1)]
        mode_str = str(self.intcode[self.pointer])[:-2][::-1] # get everything to the left of the rightmost 2 digits and reverse it
        modes = [0 if i >= len(mode_str) else int(mode_str[i]) for i in range(0, param_count)]
        debug_log(f'Operation: {op_name} with params {params} and modes {modes}')
        jump_val = op(modes)
        next_pointer = jump_val or (self.pointer + param_count + 1)
        debug_log(f'Instruction head moving to {next_pointer}')
        return next_pointer

    def send_input(self, input_code: Optional[int] = None) -> Optional[int]:
        if input_code is not None:
            self.input.append(input_code)
        return self.run_program()

    def run_program(self) -> Optional[int]:
        end = len(self.intcode)
        try:
            while self.pointer < end:
                self.pointer = self.run_instruction()
        except EndProgram:
            self.log('halt instruction received')
            return self.output
        except AwaitInput:
            self.log('awaiting input')
            return
        debug_log(f'Program ended without halt: pointer set to {self.pointer}, last available index is {end - 1}')


class Amplifier:
    def __init__(self, intcode: List[int], phase_setting: int):
        self.phase_setting = phase_setting
        self.output_signal = None
        self.halted = False
        self.computer = IntCodeComputer(intcode, phase_setting)

    def run(self, input_code: Optional[int]) -> int:
        self.output_signal = self.computer.send_input(input_code)
        if self.output_signal:
            self.halted = True
        return self.output_signal


def run_amplifiers(phase_sequence: Tuple) -> int:
    current_input = 0
    amps = [Amplifier(init_day7_data(), phase) for phase in phase_sequence]
    idx = 0
    while any([not amp.halted for amp in amps]):
        next_idx = (idx + 1) % len(amps)
        amp = amps[idx]
        amp.run(current_input)
        current_input = amp.computer.output
        idx = next_idx
    return current_input


def get_max_output_phase_sequence(phase_sequences: Iterator[Tuple]):
    return max([run_amplifiers(phase_sequence) for phase_sequence in phase_sequences])


def test_day_5_solution():
    def test_5_1_1(prog_input: int):
        IntCodeComputer([1002, 4, 3, 4, 33], prog_input).run_program()

    def test_5_1_2(prog_input: int):
        IntCodeComputer([1101, 100, -1, 4, 0], prog_input).run_program()

    def test_5_1_3(prog_input: int):
        IntCodeComputer([3, 0, 4, 0, 99], prog_input).run_program()

    def test_5_2_1(prog_input: int):
        IntCodeComputer([3,9,8,9,10,9,4,9,99,-1,8], prog_input).run_program()

    def test_5_2_2(prog_input: int):
        IntCodeComputer([3,9,7,9,10,9,4,9,99,-1,8], prog_input).run_program()

    def test_5_2_3(prog_input: int):
        IntCodeComputer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], prog_input).run_program()

    def test_5_2_4(prog_input: int):
        IntCodeComputer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], prog_input).run_program()

    def test_5_2_5(prog_input: int):
        IntCodeComputer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], prog_input).run_program()

    test_5_1_1(1) # no output, normal halt
    test_5_1_2(1) # no output, normal halt
    test_5_1_3(12) # 12

    test_5_2_1(1) # 0
    test_5_2_1(8) # 1

    test_5_2_2(9) # 0
    test_5_2_2(1) # 1

    test_5_2_3(0) # 0
    test_5_2_4(0) # 0
    test_5_2_3(1) # 1
    test_5_2_4(1) # 1

    test_5_2_5(1) # 999
    test_5_2_5(8) # 1000
    test_5_2_5(9) # 1001


def day2_part_1():
    data = init_day2_data()
    data[1] = 12
    data[2] = 2
    computer = IntCodeComputer(data, 1)
    computer.run_program()
    print(computer.intcode[0])


def day2_part_2():
    data = init_day2_data()
    computer = IntCodeComputer(data, 1)
    computer.mute()
    for noun in range(0, 100):
        for verb in range(0, 100):
            computer.intcode[1] = noun
            computer.intcode[2] = verb
            computer.run_program()
            if computer.intcode[0] == 19690720:
                print(f'100 * {noun} + {verb} = {100 * noun + verb}')
                return
            else:
                computer.reset(init_day2_data())


def day5_part_1():
    input_code = 1
    data = init_day5_data()
    computer = IntCodeComputer(data, input_code)
    computer.run_program()


def day5_part_2():
    input_code = 5
    data = init_day5_data()
    computer = IntCodeComputer(data, input_code)
    computer.mute()
    output = computer.run_program()
    print(output)


def day7_part_1():
    phase_sequences = permutations([0, 1, 2, 3, 4], 5)
    max_output = get_max_output_phase_sequence(phase_sequences)
    print(f'Largest output encountered: {max_output}')


def day7_part_2():
    phase_sequences = permutations([5, 6, 7, 8, 9], 5)
    max_output = get_max_output_phase_sequence(phase_sequences)
    print(f'Largest output encountered: {max_output}')


# day2_part_1()
# day2_part_2()
# test_day_5_solution()
# day5_part_1()
# day5_part_2()
# day7_part_1()
day7_part_2()
