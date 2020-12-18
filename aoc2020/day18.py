import operator
from typing import List, Union, Callable

import utils as U

DATA_DIR = './inputs/'


def left_math_advanced(expression: str):
    """addition precedes multiplication"""
    ops = {'+': operator.add, '*': operator.mul}
    stack = []

    def do_op(s: List[Union[str, int]]):
        # print(s)
        r_operand = int(s.pop())
        op = ops[s.pop()]
        l_operand = int(s.pop())
        s.append(op(l_operand, r_operand))
        # print(s)

    for c in expression:
        if c == ' ':
            continue
        else:
            stack.append(c)
            # print(stack)
            if c == '(':
                continue
            if c == ')':
                stack.pop()
                while stack[-2] != '(':
                    if len(stack) > 2 and stack[-2] in ops:
                        do_op(stack)
                content = stack.pop()
                stack.pop()
                stack.append(content)
            while len(stack) > 2 and stack[-2] == '+':
                do_op(stack)
    while len(stack) > 1:
        do_op(stack)
    return stack[0]


def left_math(expression: str):
    """addition and multiplication have equal precedence. Evaluation is from the left."""
    ops = {'+': operator.add, '*': operator.mul}
    stack = []
    for c in expression:
        if c == ' ':
            continue
        elif c == '(':
            stack.append(c)
            # print(stack)
            continue
        elif c == ')':
            stack.append(c)
            # print(stack)
            stack.pop()
            contents = stack.pop()
            stack.pop()
            stack.append(contents)
            # print(stack)
        elif c in ops:
            stack.append(c)
            # print(stack)
            continue
        else:
            stack.append(c)
        # print(stack)
        if len(stack) > 2 and stack[-2] in ops:
            r_operand = int(stack.pop())
            op = ops[stack.pop()]
            l_operand = int(stack.pop())
            res = op(l_operand, r_operand)
            stack.append(res)
    return stack[0]


def do_problems(problems: List[str], math: Callable):
    with U.localtimer():
        res = [math(i) for i in problems]
    # print(res)
    print(sum(res))


def __test():
    problems = U.read_path_lines(f'{DATA_DIR}test')
    do_problems(problems, left_math)
    do_problems(problems, left_math_advanced)


def __main():
    problems = U.read_path_lines(f'{DATA_DIR}day18')
    do_problems(problems, left_math)
    do_problems(problems, left_math_advanced)


if __name__ == '__main__':
    # __test()
    __main()

