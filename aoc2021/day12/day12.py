from collections import defaultdict
from typing import List, Dict, Set, Optional

sample = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

sample2 = """start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end"""


def get_input_from_file(name: str) -> Dict[str, List[str]]:
    with open(f'./{name}') as f:
        return get_adj_list(f.read())


def get_adj_list(edge_list: str) -> Dict[str, List[str]]:
    adj_list = {}
    edges = edge_list.split('\n')
    for edge in edges:
        node_a, node_b = edge.split('-')
        if node_a not in adj_list:
            adj_list[node_a] = []
        if node_b not in adj_list:
            adj_list[node_b] = []
        adj_list[node_a].append(node_b)
        adj_list[node_b].append(node_a)
    return adj_list


def get_paths(adj_list: Dict[str, List[str]], two_visits: bool = False) -> List[List[str]]:
    start = 'start'
    end = 'end'
    paths = []

    def dfs(node: str, path: str, ancestors: Dict[str, int], twice_node: str = ''):
        if node == end:
            path = path + ',' + node
            paths.append(path)
            return
        if node == start and start in ancestors:
            return
        if ancestors[node] < 1 or (two_visits and not twice_node):
            track_visits = not node.isupper()
            if track_visits:
                ancestors[node] += 1
                if ancestors[node] > 1 and two_visits and not twice_node and node != 'start':
                    twice_node = node
            if path:
                path = path + ',' + node
            else:
                path = node
            children = adj_list.get(node)
            if children:
                for child in children:
                    dfs(child, path, ancestors, twice_node)
            if track_visits:
                ancestors[node] -= 1

    dfs(start, '', defaultdict(int))
    return paths


def part1(name):
    input = get_input_from_file(name)
    paths = get_paths(input)
    print(len(paths))


def part2(name):
    input = get_input_from_file(name)
    paths = get_paths(input, two_visits=True)
    print(len(paths))


def __test():
    # part1('small_test')
    # part1('medium_test')
    # part1('large_test')
    part2('small_test')
    part2('medium_test')
    part2('large_test')


def __main():
    part1('input')
    part2('input')


if __name__ == '__main__':
    # __test()
    __main()
