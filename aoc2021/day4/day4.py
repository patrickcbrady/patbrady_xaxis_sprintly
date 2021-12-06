from collections import defaultdict
from typing import Tuple, List, Dict, Set

from utils import get_str_list

BOARD_SIZE = 5


def print_board(board: List[List[int]]):
    for row in board:
        s = ' '.join([str(c).rjust(2, ' ') for c in row])
        print(s)


def get_bingo(name: str) -> Tuple[List[int], List[List[List[int]]]]:
    strings = get_str_list(name)
    nums = [int(i) for i in strings[0].split(',')]
    boards = []
    curr_board = []
    for s in strings[2:]:
        if not s:
            boards.append(curr_board)
            curr_board = []
        else:
            curr_board.append([int(i.strip()) for i in s.split(' ') if i])
    if curr_board:
        boards.append(curr_board)
    return nums, boards


def declare_winner(board: List[List[int]], win_num: int, marked_rows: Dict[int, Set[int]],
                   marked_cols: Dict[int, Set[int]]) -> int:
    total_sum = sum(sum(r) for r in board)
    marked_sum = 0
    marked_cells = set()
    for i, cols in marked_rows.items():
        for j in cols:
            marked_cells.add((i, j))
    for j, rows in marked_cols.items():
        for i in rows:
            marked_cells.add((i, j))
    for i, j in marked_cells:
        marked_sum += board[i][j]
    unmarked_sum = total_sum - marked_sum
    return win_num * unmarked_sum


def play_bingo(nums: List[int], boards: List[List[List[int]]]) -> List[int]:
    board_to_marked_cols = defaultdict(lambda: defaultdict(set))
    board_to_marked_rows = defaultdict(lambda: defaultdict(set))
    n = len(boards)
    last_winner = None
    won_boards = set()
    win_results = []
    for num in nums:
        for b in range(n):
            if b in won_boards:
                continue
            for i in range(BOARD_SIZE):
                if b in won_boards:
                    break
                for j in range(BOARD_SIZE):
                    if boards[b][i][j] == num:
                        col_marks = board_to_marked_cols[b][j]
                        row_marks = board_to_marked_rows[b][i]
                        col_marks.add(i)
                        row_marks.add(j)
                        if len(col_marks) == BOARD_SIZE:
                            won_boards.add(b)
                            last_winner = b
                            win_results.append(
                                declare_winner(boards[b], num, board_to_marked_rows[b], board_to_marked_cols[b]))
                        if len(row_marks) == BOARD_SIZE:
                            won_boards.add(b)
                            last_winner = b
                            win_results.append(
                                declare_winner(boards[b], num, board_to_marked_rows[b], board_to_marked_cols[b]))
    print(f'last winning board: {last_winner}')
    return win_results


def run(nums: List[int], boards: List[List[List[int]]]):
    res = play_bingo(nums, boards)
    print(f'p1 solution: {res[0]}')
    print(f'p2 solution: {res[-1]}')


def __test():
    nums, boards = get_bingo('test')
    run(nums, boards)


def __main():
    nums, boards = get_bingo('input')
    run(nums, boards)


if __name__ == '__main__':
    __test()
    __main()
