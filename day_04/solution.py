#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/4

Usage: solution.py
"""


from enum import Enum
from pathlib import Path
from typing import List


class CardPart(Enum):
    """Enum to identify part of string"""

    DEALT = 0
    SOLUTION = 1
    UNKNOWN = 2


class ScratchCard:
    """Loads in a scratch card number with its solution"""

    def __init__(self, filename: str) -> None:
        self.lines: List[str] = Path(filename).read_text("utf-8").strip().split("\n")

    def get_winning_pot(self) -> int:
        """Returns total winnings"""
        winnings = 0
        for line in self.lines:
            dealt = set(self._get_dealt_hand(line))
            solution = set(self._get_winning_numbers(line))
            hits_n = len(dealt.intersection(solution))

            if hits_n > 0:
                winnings += 2 ** (hits_n - 1)

        return winnings

    def count_total_cards(self) -> int:
        """Counts the number of scratch cards"""
        cards = [1] * len(self.lines)

        for card_n, line in enumerate(self.lines):
            dealt = set(self._get_dealt_hand(line))
            solution = set(self._get_winning_numbers(line))
            hits_n = len(dealt.intersection(solution))

            if hits_n == 0:
                continue

            for i in range(card_n + 1, card_n + hits_n + 1):
                cards[i] += cards[card_n]

        return sum(cards)

    def _get_dealt_hand(self, line: str) -> List[int]:
        return self._get_numbers(CardPart.DEALT, line)

    def _get_winning_numbers(self, line: str) -> List[int]:
        return self._get_numbers(CardPart.SOLUTION, line)

    def _get_numbers(self, card_part: CardPart, line: str) -> List[int]:
        ret_val = []
        try:
            ret_val = [int(num) for num in line.split(":")[1].split("|")[card_part.value].split()]
        except IndexError:
            print(f"Cannot parse numbers from line: {line}")
        return ret_val


if __name__ == "__main__":
    assert ScratchCard("example_01.txt").get_winning_pot() == 13
    assert ScratchCard("example_02.txt").count_total_cards() == 30

    puzzle_result = ScratchCard("puzzle_input.txt")
    print(f"Total winning pot for puzzle 01: {puzzle_result.get_winning_pot()}")
    print(f"Total winning pot for puzzle 01: {puzzle_result.count_total_cards()}")
