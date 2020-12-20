from typing import List, Dict, Callable, Tuple

import utils as U

DATA_DIR = './inputs/'

rule_31_matches_19b = {'abbabbbb', 'bbbbabbb', 'babbbbbb', 'bbbbaaba', 'aabaabab', 'baabbbbb', 'abbabbab', 'babbaabb', 'bbbbabba', 'bbbabbba', 'aabaabba', 'abaabaab', 'bababbba', 'bbbbbaab', 'aabbabab', 'babbbaba', 'babaabbb', 'aabbbaba', 'abbabbaa', 'baaaaabb', 'aaaaabbb', 'aabbbabb', 'aababbba', 'abbaabba', 'babaaabb', 'aabaaaaa', 'abbbaaba', 'baabaabb', 'aaabbbba', 'aaabbbaa', 'aaabbbbb', 'baaaaaba', 'bbbbbbbb', 'aaaaabaa', 'baabbaba', 'bbbbabaa', 'bbabbbbb', 'babbbbaa', 'aaaabaaa', 'abaabaaa', 'baababba', 'aabbaaba', 'bbbabbaa', 'aabbaaab', 'bbbaabab', 'baaaaaab', 'aaabaaab', 'abbaabab', 'abbababa', 'abbbbbab', 'aabaaabb', 'bbaaabaa', 'abbbbaaa', 'baaaabaa', 'abaaaaab', 'abaabbaa', 'babaabab', 'bbaabaaa', 'baaabbab', 'aaabbaba', 'bbababaa', 'baaaabab', 'aabaaaba', 'babbabba', 'bbababbb', 'abbbbaba', 'baabbabb', 'bbabbabb', 'bbbbbaba', 'bbabbbba', 'abbbabbb', 'bbbaabbb', 'aabbbbba', 'abaaabbb', 'aabbaabb', 'bbbbaabb', 'abaaabab', 'abababaa', 'abbaabaa', 'aaaababa', 'aababaaa', 'bbbabaaa', 'ababaaba', 'bbaaaaba', 'bbbabbbb', 'babbaaba', 'abbaaabb', 'abbaaaab', 'aabaabaa', 'bbaabaab', 'ababbabb', 'bbaababb', 'aababaab', 'ababbbba', 'aaaaabba', 'baabaaab', 'aaaaabab', 'babbbaab', 'bbaabbab', 'bbbbbbab', 'bbbababb', 'ababbaab', 'abbbbbaa', 'ababbaba', 'baaaaaaa', 'babaabba', 'bbaabbbb', 'bbaabbba', 'baaabaab', 'baababbb', 'baaaabba', 'babbbabb', 'baaabbba', 'baabbbab', 'abaabbbb', 'baabbaaa', 'abbabbba', 'bbaabbaa', 'abaabbba', 'baabbbaa', 'abababba', 'abbbaaaa', 'aaaaaaaa', 'baaababa'}
rule_42_matches_19b = {'aaabaabb', 'aabbbbbb', 'abbbbabb', 'bbabaaaa', 'bbbaabaa', 'bbabaabb', 'bbbbbabb', 'babababa', 'aaabaaba', 'abbaabbb', 'babbaaaa', 'baaabbaa', 'aabababb', 'abbbabba', 'aabbabba', 'ababaaab', 'abbaaaaa', 'baaabbbb', 'baabbbba', 'abbbaabb', 'bbabbbaa', 'babaaaba', 'aabbbaab', 'bbaaabba', 'abaababb', 'aabaaaab', 'abbbbaab', 'aaaaaaba', 'abbbabab', 'aababbbb', 'aaabbbab', 'baababab', 'babaaaaa', 'abbabaab', 'bbbbaaab', 'aaabaaaa', 'baabaaaa', 'aaabbaab', 'bbabbaba', 'ababaaaa', 'aabaabbb', 'bbbaaabb', 'bbababab', 'bbbbbbaa', 'bababbbb', 'aaaababb', 'bababaab', 'bbbababa', 'babbbaaa', 'abaabbab', 'ababbbbb', 'baababaa', 'abaaabaa', 'aaababba', 'bbbbbaaa', 'baabaaba', 'ababbaaa', 'baabbaab', 'babbabab', 'bbabbaaa', 'aababbab', 'abbbabaa', 'abaaabba', 'bbaaabab', 'ababaabb', 'aaaabaab', 'bbbaaaba', 'aaabbaaa', 'babaaaab', 'aabbbaaa', 'bababaaa', 'bbabbbab', 'abaaaaba', 'ababbbab', 'bbbabaab', 'abbaaaba', 'baaabaaa', 'abaaaaaa', 'bbababba', 'aaaabbab', 'aabbbbaa', 'bbabaaab', 'aabababa', 'aaaabbaa', 'abbbaaab', 'baaaabbb', 'aaababab', 'bbaababa', 'bbbbabab', 'aaaaaabb', 'bbaaaaaa', 'bbbbaaaa', 'aaababbb', 'bbbbbbba', 'babbaaab', 'bbaaaaab', 'bababbab', 'aaabbabb', 'bbbaaaaa', 'aaaabbba', 'abbbbbbb', 'abbababb', 'bbabbaab', 'aabbabbb', 'bbabaaba', 'baaababb', 'aabbbbab', 'babbabaa', 'aabbaaaa', 'bababbaa', 'babaabaa', 'abaaaabb', 'abababab', 'aabbabaa', 'babbabbb', 'aaababaa', 'aaaaaaab', 'aaaabbbb', 'bbbaabba', 'bbbaaaab', 'babababb', 'babbbbab', 'abbbbbba', 'babbbbba', 'bbaaabbb', 'bbaaaabb', 'abaababa', 'aababbaa'}

class RuleSet:
    def __init__(self, rules: List[str]):
        self.match_idx = 0
        self.last_char_match = None
        self.rules = self._init_rules(rules)
        self.matches_42 = set()
        self.matches_31 = set()

    def hit_the_end(self, s: str):
        print('hit the end!')
        return False

    def make_base_rule(self, match_char: str) -> Callable:
        def rule_func(s: str) -> bool:
            if self.match_idx == len(s):
                return self.hit_the_end(s)
            # if s == 'aaaabbaaaabbaaa':
            # print(f'Checking if {s[0:self.match_idx]}[{s[self.match_idx]}]{s[(self.match_idx + 1):]} == {match_char}')
            rule_match = s[self.match_idx] == match_char
            self.last_char_match = rule_match
            if rule_match:
                self.match_idx += 1
                return rule_match
            return rule_match
        return rule_func

    def make_sequence_rule(self, rule_str: str) -> Callable:
        rule_seq = [int(i) for i in rule_str.split(' ')]
        def rule_func(s: str) -> bool:
            if self.match_idx == len(s):
                return self.hit_the_end(s)
            if all(self.rules[r](s) for r in rule_seq):
                return True
            return False
        return rule_func

    def make_or_rule(self, rule_str: str, idx: int):
        def log(msg: str):
            if idx in (31, 42):
                print(msg)

        def rule_func(s: str) -> bool:
            # log(f'evaluating {idx}')


            if self.match_idx == len(s):
                # log('hitting the end')
                return False
            match_idx = self.match_idx
            step_seq_a, step_seq_b = tuple([int(i) for i in seq.split(' ')] for seq in rule_str.split(' | '))
            if all(self.rules[r](s) for r in step_seq_a):
                if idx == 31:
                    self.matches_31.add(s[match_idx:self.match_idx])
                if idx == 42:
                    self.matches_42.add(s[match_idx: self.match_idx])
                # log(f'matched first branch: evaluated {s[match_idx:self.match_idx]}')
                return True
            self.match_idx = match_idx
            if all(self.rules[r](s) for r in step_seq_b):
                if idx == 31:
                    self.matches_31.add(s[match_idx:self.match_idx])
                if idx == 42:
                    self.matches_42.add(s[match_idx: self.match_idx])
                # log(f'matched second branch: evaluated {s[match_idx:self.match_idx]}')
                return True
            # log('returning False early')
            return False
        return rule_func

    def _init_rules(self, rules: List[str]) -> Dict[int, Callable]:
        res = {}
        for rule in rules:
            idx, rule_str = tuple(rule.split(': '))
            if '"' in rule_str:
                match_char = rule_str[rule_str.index('"') + 1]
                run_rule = self.make_base_rule(match_char)
            elif '|' in rule_str:
                run_rule = self.make_or_rule(rule_str, int(idx))
            else:
                run_rule = self.make_sequence_rule(rule_str)
            res[int(idx)] = run_rule
        return res

    def check_message(self, msg: str) -> bool:
        pointer_a = -8
        pointer_b = len(msg)
        num_31s = 0
        if msg[pointer_a:pointer_b] not in rule_31_matches_19b:
            return False
        while msg[pointer_a:pointer_b] in rule_31_matches_19b:
            num_31s += 1
            pointer_a -= 8
            pointer_b -= 8
        num_42s = 0
        pointer_a = 0
        pointer_b = 8
        if msg[pointer_a:pointer_b] not in rule_42_matches_19b:
            return False
        while msg[pointer_a:pointer_b] in rule_42_matches_19b:
            num_42s += 1
            pointer_a += 8
            pointer_b += 8
        # print(f'42s: {num_42s}, 31s: {num_31s}, sub_lens: {(num_42s + num_31s) * 8}, len: {len(msg)}')
        if num_42s > num_31s and ((num_42s + num_31s) * 8) == len(msg):
            return True
        return False

        # self.last_char_match = None
        # self.match_idx = 0
        # print(f'Checking {msg}')
        # self.rules[0](msg)
        # print(f'done: {self.last_char_match}')
        # return self.last_char_match and self.match_idx == len(msg)


def part1(rules: List[str], messages: List[str]):
    rule_set = RuleSet(rules)
    res = [m for m in messages if rule_set.check_message(m)]
    print(len(res))
    # print(f'31: {rule_set.matches_31}')
    # print(f'42: {rule_set.matches_42}')


def _run_program(input_path: str):
    rules, messages = tuple(U.read_chunked_lines(input_path))
    rules = rules.split('\n')
    messages = messages.split('\n')
    part1(rules, messages)


def __test():
    _run_program(f'{DATA_DIR}test')


def __main():
    _run_program(f'{DATA_DIR}day19b')


if __name__ == '__main__':
    # __test()
    __main()
