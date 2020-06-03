from typing import Callable
import utils.core.utils as U

DATA_DIR = './'
PASSWORD_LEN = 6


def read_input_data(filename: str):
    data = open(f'{DATA_DIR}/{filename}', 'r').read().split('-')
    return range(int(data[0]), int(data[1]))


def read_test_data(filename: str):
    data = open(f'{DATA_DIR}/{filename}', 'r').read().split('\n')
    return [int(x) for x in data]


def check_number(num: int) -> bool:
    num_str = str(num)
    has_double = False

    if len(num_str) != PASSWORD_LEN:
        return False

    prev_num = '0'
    for digit in num_str:
        if int(digit) < int(prev_num):
            return False
        if digit == prev_num:
            has_double = True
        prev_num = digit

    return has_double


def check_number_part2(num: int) -> bool:
    num_str = str(num)
    has_double = False

    if len(num_str) != PASSWORD_LEN:
        return False

    same_counter = 0
    prev_num = '0'
    for digit in num_str:
        if int(digit) < int(prev_num):
            return False

        if digit == prev_num:
            same_counter += 1
        else:
            if same_counter == 1:
                has_double = True
            same_counter = 0
        prev_num = digit

    return has_double or same_counter == 1


def test_check_number_part1():
    data = read_test_data('day_4_test')
    assert check_number(data[0]) is True
    assert check_number(data[1]) is False
    assert check_number(data[2]) is False


def test_check_number_part2():
    assert check_number_part2(112233) is True
    assert check_number_part2(123444) is False
    assert check_number_part2(111122) is True


@U.timer
def print_password_count(validate: Callable):
    input_range = read_input_data('day_4_input')
    possible_passwords = []
    for num in input_range:
        if validate(num):
            possible_passwords.append(num)

    print(f'Number of potential passwords: {len(possible_passwords)}')


def part_1():
    print_password_count(check_number)


def part_2():
    print_password_count(check_number_part2)


def __main():
    part_1()
    part_2()


if __name__ == '__main__':
    __main()
