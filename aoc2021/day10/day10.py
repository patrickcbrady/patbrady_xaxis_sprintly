from typing import List, Tuple


def get_lines(name: str) -> List[str]:
    with open(f'./{name}') as f:
        return f.read().split('\n')


def check_line(line: str) -> Tuple[int, List[str]]:
    open_to_close = {'(': ')',
                     '{': '}',
                     '[': ']',
                     '<': '>'}
    err_to_score = {')': 3,
                    ']': 57,
                    '}': 1197,
                    '>': 25137}
    stack = []
    closers = set(open_to_close.values())
    for c in line:
        if c in open_to_close:
            stack.append(open_to_close[c])
        elif c in closers:
            if c != stack[-1]:
                return err_to_score[c], []
            else:
                stack.pop()
    return 0, stack[::-1]


def part1(name: str):
    lines = get_lines(name)
    total = 0
    for line in lines:
        score, _ = check_line(line)
        total += score
    print(total)


def part2(name: str):
    lines = get_lines(name)
    char_to_points = {')': 1, ']': 2, '}': 3, '>': 4}
    scores = []
    for line in lines:
        score = 0
        errs, stack = check_line(line)
        if errs == 0:
            for c in stack:
                score *= 5
                score += char_to_points[c]
            scores.append(score)
    scores = sorted(scores)
    n = len(scores)
    if n % 2 == 0:
        middle = (scores[n // 2] + scores[n // 2 - 1]) / 2
    else:
        middle = scores[n // 2]
    print(middle)


def __test():
    part1('large_test')
    part2('large_test')


def __main():
    part1('input')
    part2('input')


if __name__ == '__main__':
    __test()
    __main()
