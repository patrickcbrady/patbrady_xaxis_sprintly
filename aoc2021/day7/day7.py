import math
from typing import List

from utils import get_int_list_from_csv


def get_kth_smallest(arr: List[int], k: int):
    def swap(a: int, b: int):
        temp = arr[a]
        arr[a] = arr[b]
        arr[b] = temp

    n = len(arr)
    left = 0
    right = n - 1
    while left <= right:
        pivot = (left + right) // 2
        pivot_val = arr[pivot]
        swap(pivot, right)
        lo = left
        for i in range(left, right):
            if arr[i] < pivot_val:
                swap(i, lo)
                lo += 1
        eq = lo
        for j in range(eq, right + 1):
            if arr[j] == pivot_val:
                swap(j, eq)
                eq += 1

        if k < lo:
            right = lo - 1
        elif k < eq:
            return arr[lo]
        else:
            left = lo + 1


def get_kth_largest(arr: List[int], k: int):
    return get_kth_smallest(arr, len(arr) - 1 - k)

# positions = get_int_list_from_csv('test')
positions = get_int_list_from_csv('input')
avg = round(sum(positions) / len(positions))
# k = len(positions) // 2
# median = get_kth_smallest(positions, k)
# med_fuel_cost = sum(abs(i - median) for i in positions)
# print(f'median_pos: {k}, median_val: {median}')
# print(med_fuel_cost)


def get_cost(n: int):
    return (n * (n + 1)) / 2


avg_fuel_cost = round(sum(get_cost(abs(i - avg)) for i in positions))
print(f'avg_val: {avg}')
print(avg_fuel_cost)