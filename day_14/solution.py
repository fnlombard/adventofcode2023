#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/14

Usage: solution.py
"""

from enum import Enum, auto
from pathlib import Path
from typing import List

import numpy as np


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


class Element(Enum):
    SPACE = auto()
    CUBE = auto()
    BOULDER = auto()


class Board:
    def __init__(self, board_data: List[str]) -> None:
        self.content = np.array([
            [self._map_to_element(character) for character in line]
            for line in board_data
        ])

    def _map_to_element(self, character: str) -> Element:
        if character == '.':
            return Element.SPACE
        elif character == 'O':
            return Element.BOULDER
        elif character == '#':
            return Element.CUBE
        else:
            raise RuntimeError(f"Unkown character: {character}")

    def _map_from_element(self, element: Element) -> str:
        if element == Element.BOULDER:
            return "O"
        elif element == Element.CUBE:
            return "#"
        elif element == Element.SPACE:
            return "."
        else:
            raise RuntimeError(f"Unkown element: {element}")

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(
                self._map_from_element(element) for element in line)
            for line in self.content
        )

    def get_load(self) -> int: ...

    def tilt(self, direction: Direction = Direction.NORTH) -> None:
        if direction == Direction.NORTH:
            for r_i, row in enumerate(self.content):
                for c_i, element in enumerate(row):
                    if element == Element.BOULDER:
                        self._shift(row=r_i + 1, column=c_i, direction=direction)

    def _shift(self, row: int, column: int, direction: Direction = Direction.NORTH) -> None:
        if row < 0 or row >= self.content.shape[0]:
            return
        if column < 0 or column >= self.content.shape[0]:
            return
        if self.content[row][column] == Element.SPACE:
            if direction == Direction.NORTH:
                return self._shift(row=row+1, column=column, direction=direction)
        elif self.content[row][column] in [Element.BOULDER, Element.CUBE]:
            return
        else:
            raise RuntimeError(f"Unknown element: {self.content[row][column]}")


class Solution:
    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text('utf-8').strip().split('\n')
        self.board = Board(board_data=file_contents)

    def puzzle_01(self) -> int:
        self.board.tilt()
        return self.board.get_load()


if __name__ == '__main__':
    assert Solution("example.txt").puzzle_01() == 136

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.puzzle_01()}")
