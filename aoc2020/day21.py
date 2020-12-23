from collections import defaultdict, OrderedDict
from typing import List

import utils as U

DATA_DIR = './inputs/'


def part1(lines: List[str]):
    ings = defaultdict(int)
    algns = set()
    algn_to_ingr = {}
    ingr_to_algn = {}
    for line in lines:
        ingredients, allergens = tuple(line.split(' (contains '))
        ingredients = set(ingredients.split(' '))
        allergens = set(allergens[:-1].split(', '))
        algns = algns | allergens
        for a in allergens:
            if algn_to_ingr.get(a):
                algn_to_ingr[a] = algn_to_ingr[a] & ingredients
            else:
                algn_to_ingr[a] = ingredients
        for i in ingredients:
            ings[i] += 1

    while any(len(i) > 1 for i in algn_to_ingr.values()):
        ing_sets = algn_to_ingr.values()
        for ingredients in ing_sets:
            if len(ingredients) > 1:
                continue
            for a in algn_to_ingr:
                if len(algn_to_ingr[a]) > 1:
                    algn_to_ingr[a] = algn_to_ingr[a] - ingredients

    for i in ings:
        ingr_to_algn[i] = set()
        for a, ing_set in algn_to_ingr.items():
            if i in ing_set:
                ingr_to_algn[i].add(a)

    total_no_algns = 0
    for ing, count in ings.items():
        if not ingr_to_algn[ing]:
            total_no_algns += count

    # print(algn_to_ingr)
    # print(ingr_to_algn)
    print(total_no_algns)
    dangerous = OrderedDict(sorted(algn_to_ingr.items()))
    print(','.join(i for k, v in dangerous.items() for i in v))


def _run_program(input_path: str):
    in_file = U.read_path_lines(input_path)
    part1(in_file)


def __test():
    _run_program(f'{DATA_DIR}test')


def __main():
    _run_program(f'{DATA_DIR}day21')


if __name__ == '__main__':
    # __test()
    __main()
