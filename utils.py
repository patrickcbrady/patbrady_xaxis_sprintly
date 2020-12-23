import time
from contextlib import contextmanager
from typing import List, Tuple


def read_whole_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()


def read_path(file_path: str, splitter: str) -> List[str]:
    with open(file_path, 'r') as f:
        return f.read().split(splitter)


def read_path_lines(file_path: str) -> List[str]:
    return read_path(file_path, '\n')


def read_path_blank_lines(file_path: str) -> List[str]:
    return [s.replace('\n', ' ') for s in read_path(file_path, '\n\n')]


def read_chunked_lines(file_path: str) -> List[str]:
    return read_path(file_path, '\n\n')


def read_path_csv(file_path: str) -> List[str]:
    return read_path(file_path, ',')


@contextmanager
def localtimer():
    start = time.perf_counter()
    yield
    print('func took', time.perf_counter() - start)
