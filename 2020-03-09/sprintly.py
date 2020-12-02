from typing import List

DATA_DIR = './'
OPERATIONS = {'<': lambda x, y: x < y,
              '<=': lambda x, y: x <= y,
              '>': lambda x, y: x > y,
              '>=': lambda x, y: x >= y,
              '==': lambda x, y: x == y,
              '!=': lambda x, y: x != y,
              'inc': lambda x, y: x + y,
              'dec': lambda x, y: x - y}


def read_input_data(filename: str) -> List[str]:
    data = open(f'{DATA_DIR}/{filename}', 'r').read()
    return str(data).split('\n')


def read_instruction(i: str):
    components = i.split(' ')
    curr_op = None
    for c in components:
        if c in OPERATIONS:
            curr_op = OPERATIONS[c]


test_input = read_input_data('test-input')
print(test_input)
