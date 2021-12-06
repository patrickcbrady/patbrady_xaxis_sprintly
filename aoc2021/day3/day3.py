from typing import List, Dict

from utils import get_str_list


def count_bits_per_pos(report: List[str]) -> Dict[int, Dict[str, int]]:
    pos_to_val_to_count = {}
    for num in report:
        for i, c in enumerate(num):
            if i not in pos_to_val_to_count:
                pos_to_val_to_count[i] = {}
            if c not in pos_to_val_to_count[i]:
                pos_to_val_to_count[i][c] = 0
            pos_to_val_to_count[i][c] += 1
    return pos_to_val_to_count


def get_gas_ratings(report: List[str], most_common: bool = True) -> str:
    n = len(report[0])
    remaining = report
    for pos in range(n):
        counts = {}
        lists = {}
        for b_str in remaining:
            if b_str[pos] not in counts:
                counts[b_str[pos]] = 0
            if b_str[pos] not in lists:
                lists[b_str[pos]] = []
            counts[b_str[pos]] += 1
            lists[b_str[pos]].append(b_str)
        if counts['1'] >= counts['0']:
            digit = '1' if most_common else '0'
        else:
            digit = '0' if most_common else '1'
        remaining = lists[digit]
        if len(remaining) == 1:
            return remaining[0]


def get_power_consumption(report: List[str]):
    pos_to_val_to_count = count_bits_per_pos(report)
    gamma = []
    epsilon = []
    for _, val_to_count in pos_to_val_to_count.items():
        count_to_val = {v: k for k, v in val_to_count.items()}
        gamma.append(count_to_val[max(count_to_val)])
        epsilon.append(count_to_val[min(count_to_val)])
    return int(''.join(gamma), 2) * int(''.join(epsilon), 2)


def run(report: List[str]):
    result = get_power_consumption(report)
    print(result)
    oxygen = get_gas_ratings(report)
    co2 = get_gas_ratings(report, False)
    life_support = int(oxygen, 2) * int(co2, 2)
    print(life_support)


def __test():
    report = get_str_list('test')
    run(report)


def __main():
    report = get_str_list('input')
    run(report)


if __name__ == '__main__':
    __test()
    __main()
