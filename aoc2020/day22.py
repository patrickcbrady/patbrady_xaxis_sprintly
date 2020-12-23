from collections import deque
from itertools import count
from typing import Dict, Optional, Tuple

from dataclasses import dataclass

import utils as U

DATA_DIR = './inputs/'
IDENTIFIERS = count(start=2)


def print_decks(p1: deque, p2: deque):
    print(f'Player 1\'s deck: {", ".join(str(c) for c in p1)}')
    print(f'Player 2\'s deck: {", ".join(str(c) for c in p2)}')


def print_scores(p1: deque, p2: deque):
    print(f'Player 1\'s score: {calc_score(p1)}')
    print(f'Player 2\'s score: {calc_score(p2)}')


def calc_score(deck: deque) -> int:
    return sum((len(deck) - i) * v for i, v in enumerate(deck))


@dataclass
class CombatGame:
    p1_deck: deque
    p2_deck: deque
    id: int = 1
    round: int = 0
    logging: bool = False
    deck_to_round: Optional[Dict[Tuple[int, ...], int]] = None

    @property
    def deck_tuple(self) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        """return the contents of p1's deck followed by the contents of p2's deck, as a tuple"""
        return tuple(self.p1_deck), tuple(self.p2_deck)

    def log(self, msg):
        if self.logging:
            print(msg)

    def print_decks(self):
        if self.logging:
            print_decks(self.p1_deck, self.p2_deck)

    def print_scores(self):
        if self.logging:
            print_scores(self.p1_deck, self.p2_deck)

    def draw_cards(self):
        p1_turn, p2_turn = self.p1_deck.popleft(), self.p2_deck.popleft()
        self.log(f'Player 1 plays: {p1_turn}')
        self.log(f'Player 2 plays: {p2_turn}')
        return p1_turn, p2_turn

    def play_normal(self):
        while self.p1_deck and self.p2_deck:
            self.round += 1
            self.log(f'-- Round {self.round} --')
            self.print_decks()
            p1_turn, p2_turn = self.draw_cards()
            round_winner = 1 if p1_turn > p2_turn else 2
            self.log(f'Player {round_winner} wins round {self.round} of game {self.id}!')
            self.end_round(round_winner, p1_turn, p2_turn)
        self.print_results()

    def end_round(self, round_winner: int, p1_turn: int, p2_turn: int):
        if round_winner == 1:
            self.p1_deck.extend([p1_turn, p2_turn])
        else:
            self.p2_deck.extend([p2_turn, p1_turn])

    def record_decks(self):
        self.deck_to_round[self.deck_tuple] = self.round

    def check_for_p1_win(self) -> bool:
        return self.deck_to_round.get(self.deck_tuple, False)

    def play_recursive(self):
        self.play_recursive_rounds()
        self.print_results()

    def play_recursive_rounds(self) -> int:
        self.log(f'\n=== Game {self.id} ===')
        self.deck_to_round = {}
        while len(self.p1_deck) > 0 and len(self.p2_deck) > 0:
            self.round += 1
            self.log(f'\n-- Round {self.round} (Game {self.id}) --')
            self.print_decks()
            if self.check_for_p1_win():
                return self.win_by_same_game()
            self.record_decks()
            p1_turn, p2_turn = self.draw_cards()
            if len(self.p1_deck) >= p1_turn and len(self.p2_deck) >= p2_turn:
                self.log('Playing a sub-game to determine the winner...')
                recurse_game = CombatGame(deque(list(self.p1_deck)[0:p1_turn]), deque(list(self.p2_deck)[0:p2_turn]),
                                          id=next(IDENTIFIERS), logging=self.logging)
                round_winner = recurse_game.play_recursive_rounds()
                self.log(f'\n...anyway, back to game {self.id}.')
            else:
                round_winner = 1 if p1_turn > p2_turn else 2
            self.log(f'Player {round_winner} wins round {self.round} of game {self.id}!')
            self.end_round(round_winner, p1_turn, p2_turn)
        if len(self.p1_deck) == 0:
            game_winner = 2
        else:
            game_winner = 1
        self.log(f'The winner of game {self.id} is player {game_winner}!')
        return game_winner

    def win_by_same_game(self) -> int:
        self.log('Player 1 wins by round repetition')
        self.log(
            f'In round {self.round} of game {self.id}, the same decks repeated as in round {self.deck_to_round[self.deck_tuple]}')
        return 1

    def print_results(self):
        print('\n')
        print('== Post-game results ==')
        logging = self.logging
        self.logging = True
        self.print_decks()
        self.print_scores()
        self.logging = logging


def part1(p1_deck: deque, p2_deck: deque):
    cg = CombatGame(p1_deck, p2_deck, logging=False)
    # cg.play_normal()
    cg.play_recursive()


def _run_program(input_path):
    input_lines = U.read_path_lines(input_path)
    p1_deck_start = input_lines.index('Player 1:') + 1
    p2_deck_start = input_lines.index('Player 2:') + 1
    p1_deck = deque(int(i) for i in input_lines[p1_deck_start: p2_deck_start - 2])
    p2_deck = deque(int(i) for i in input_lines[p2_deck_start:])
    part1(p1_deck, p2_deck)


def __test():
    _run_program(f'{DATA_DIR}test')


def __main():
    _run_program(f'{DATA_DIR}day22')


if __name__ == '__main__':
    # __test()
    __main()
