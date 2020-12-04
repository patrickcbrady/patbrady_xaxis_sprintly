import re
from typing import List, NamedTuple, Dict, Set, Callable, Optional

from utils import read_path_blank_lines, localtimer

DATA_DIR = './inputs/'


class Passports(NamedTuple):
    passports: List[Dict[str, str]]

    @classmethod
    def from_str_list(cls, passports: List[str]) -> 'Passports':
        res = []
        for p in passports:
            pairs = p.split(' ')
            passport = {k: v for k, v in [tuple(pair.split(':')) for pair in pairs]}
            res.append(passport)
        return cls(res)

    @property
    def required_keys(self) -> Set[str]:
        return {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

    @staticmethod
    def validate(p: Dict[str, str]) -> bool:
        def validate_yr(yr: str, min: int, max: int) -> bool:
            return len(yr) == 4 and min <= int(yr) <= max

        def validate_hgt(hgt: str) -> bool:
            if hgt[-2:] not in ('cm', 'in'):
                return False
            minmax_dict = {'cm': (150, 193), 'in': (59, 76)}
            min, max = minmax_dict[hgt[-2:]]
            return min <= int(hgt[:-2]) <= max

        def validate_hcl(hcl: str) -> bool:
            return re.match('#[0-9a-f]{6}$', hcl) is not None

        def validate_ecl(ecl: str) -> bool:
            return ecl in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

        def validate_pid(pid: str) -> bool:
            return re.match('[0-9]{9}$', pid) is not None

        return (validate_yr(p['byr'], 1920, 2002) and validate_yr(p['iyr'], 2010, 2020)
                and validate_yr(p['eyr'], 2020, 2030) and validate_hgt(p['hgt']) and validate_hcl(p['hcl'])
                and validate_ecl(p['ecl']) and validate_pid(p['pid']))

    def valid_count(self, validator: Optional[Callable] = None) -> int:
        res = 0
        for p in self.passports:
            if not self.required_keys - set(p):
                if validator is None or validator(p):
                    res += 1
        return res


def part1(passports: List[str]):
    passports = Passports.from_str_list(passports)
    with localtimer():
        res = passports.valid_count()
    print(f'Number of valid passports: {res}')


def part2(passports: List[str]):
    passports = Passports.from_str_list(passports)
    with localtimer():
        res = passports.valid_count(Passports.validate)
    print(f'Number of valid passports: {res}')


def __main():
    passports = read_path_blank_lines(f'{DATA_DIR}day4')
    part1(passports)
    part2(passports)


if __name__ == '__main__':
    __main()
