DATA_DIR = './'

data = open(f'{DATA_DIR}/input1', 'r').read().split('\n')
data = [int(d) for d in data if d]


def calc_fuel(mass: int):
    return int(mass / 3) - 2


def calc_full_fuel(mass: int):
    res = 0
    fuel = calc_fuel(mass)
    while fuel > 0:
        res += fuel
        fuel = calc_fuel(fuel)
    return res


def part1():
    return sum([calc_fuel(mass) for mass in data])


def part2():
    return sum([calc_full_fuel(mass) for mass in data])


print(part1())
print(part2())
