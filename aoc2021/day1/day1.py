from typing import List

from utils import get_int_list


def count_increases(arr: List[int]) -> int:
    count = 0
    for i in range(1, len(arr)):
        if arr[i] > arr[i - 1]:
            count += 1
    return count


def count_increasing_windows(arr: List[int]) -> int:
    count = 0
    prev_window = None
    for i in range(2, len(arr)):
        curr_window = arr[i] + arr[i - 1] + arr[i - 2]
        if prev_window is not None:
            if curr_window > prev_window:
                count += 1
        prev_window = curr_window
    return count


def __test():
    input = get_int_list('test')
    print(count_increases(input))
    print(count_increasing_windows(input))


def __main():
    input = get_int_list('input.txt')
    print(count_increases(input))
    print(count_increasing_windows(input))


if __name__ == '__main__':
    __test()
    __main()
