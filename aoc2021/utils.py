from typing import List, Callable, TypeVar, Tuple

R = TypeVar('R')
Coords = Tuple[Tuple[int, int], Tuple[int, int]]


def _get_int_list_from_str(s: str) -> List[int]:
    return [int(line) for line in s.split('\n')]


def _get_arg_list_from_str(s: str) -> List[List[str]]:
    return [line.split(' ') for line in s.split('\n')]


def _get_str_list_from_str(s: str) -> List[str]:
    return [line for line in s.split('\n')]


def _get_coord_line_list_from_str(s: str) -> List[Coords]:
    def get_coords(coord_str: str) -> Tuple[int, int]:
        a, b = tuple(coord_str.split(','))
        return int(a), int(b)
    line_coords = [tuple(line.split(' -> ')) for line in s.split('\n')]
    return [(get_coords(a), get_coords(b)) for a, b in line_coords]


def process_text_file(name: str, func: Callable[[str], R]) -> R:
    with open(f'./{name}', 'r') as text_file:
        return func(text_file.read())


def get_int_list(name: str) -> List[int]:
    return process_text_file(name, _get_int_list_from_str)


def get_arg_list(name: str) -> List[List[str]]:
    return process_text_file(name, _get_arg_list_from_str)


def get_str_list(name: str) -> List[str]:
    return process_text_file(name, _get_str_list_from_str)


def get_coord_line_list(name: str) -> List[Coords]:
    return process_text_file(name, _get_coord_line_list_from_str)