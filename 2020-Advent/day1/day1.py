from typing import List, Tuple, Optional

from utils import read_path_lines, localtimer

DATA_DIR = './'

__author__ = 'patrickcbrady'


def get_summands(num_list: List[int], goal_value: int, num_summands: int = 2) -> Tuple[int, ...]:
    """
    return a Tuple of num_summands integers that exist in num_list and add up to goal_value
    recursive general solution using sets that does not require sorting.
    Worst case could be O(n**(num_summands-1)) but for the problem at hand it's faster than the sorted solution
    and for the default case of 2 summands it should be O(n)
    """
    if num_summands == 2:
        num_set = set(num_list)
        if goal_value % 2 == 0:
            # check to see whether there are 2 duplicate values that add up to goal_value
            half = goal_value // 2
            if half in num_set and num_list.count(half) > 1:
                return half, half
        for num in num_set:
            # by checking for duplicate numbers above, we are now sure that if there is a result,
            # it will be two different numbers, so we can use diff != num to avoid matching a number with itself
            diff = goal_value - num
            if diff in num_set and diff != num:
                return num, goal_value - num
    else:
        while len(num_list) > num_summands:
            # remove a number from the end of the list, then check if there is a set of num_summands - 1 numbers
            # in the remaining list that add up to goal_value - number. If yes, return. If no, remove another number.
            num = num_list.pop()
            new_goal = goal_value - num
            if new_goal < 0:
                # don't bother recursing if the goal is impossible
                # assumes all "expense report" entries must be positive
                continue
            res = get_summands(list(num_list), new_goal, num_summands-1)
            if res is not None:
                return (num,) + res


def binary_search(arr, low, high, x):
    """
    return the index of x if it exists in arr, else return -1
    uses binary search for O(log(n)) performance
    """
    if high >= low:
        mid = (high + low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        return -1


def get_3_summands(num_list: List[int], goal_value: int) -> Optional[Tuple[int, int, int]]:
    """
    return a Tuple of 3 numbers that exist in num_list and add up to goal_value, if they exist in the list
    requires sorting the list and uses a combination of small and big pointers with binary search to comb the list
    for 3 numbers. Should have worst case performance of O(n(log(n)) due to the sorting as well as running
    up to n iterations of O(log(n)) binary search
    """
    nums_asc = sorted(num_list)
    small = 0
    big = len(nums_asc) - 1

    def get_sum(s: int, m: int, b: int) -> int:
        return nums_asc[s] + nums_asc[m] + nums_asc[b]

    while small < big:
        desired_value = (goal_value - nums_asc[small]) - nums_asc[big]
        if desired_value < 1:
            big -= 1
            continue
        if desired_value > nums_asc[big]:
            small += 1
            continue

        middle = binary_search(nums_asc, small + 1, big - 1, desired_value)
        if middle != -1:
            return nums_asc[small], nums_asc[middle], nums_asc[big]
        else:
            middle = small + big // 2
            if get_sum(small, middle, big) < goal_value:
                small += 1
            else:
                big -= 1

    return None


def part1(num_list: List[int], goal_value: int):
    with localtimer():
        a, b = get_summands(num_list, goal_value)
    print(f'2 summands are {a}, {b}')
    print(a * b)


def part2(num_list: List[int], goal_value: int):
    with localtimer():
        a, b, c = get_summands(num_list, goal_value, 3)
    print(f'3 summands are {a}, {b}, {c}')
    print(a * b * c)


def __main():
    num_list = list(map(int, read_path_lines(f'{DATA_DIR}input')))
    goal_value = 2020
    part1(num_list, goal_value)
    part2(num_list, goal_value)


if __name__ == '__main__':
    __main()
