#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/14

Usage: solution.py
"""

from contextlib import contextmanager
from enum import Enum, auto
from pathlib import Path
from typing import Iterator, List, Tuple

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

    @contextmanager
    def boulder_positions(self, direction: Direction) -> Iterator[List[Tuple[int, int]]]:
        try:
            positions = []
            row_n, col_n = self.content.shape
            if direction == Direction.NORTH or direction == Direction.SOUTH:
                rows = range(1, row_n) if direction == Direction.NORTH else range(row_n - 2, -1, -1)
                for c_i in range(col_n):
                    for r_i in rows:
                        if self.content[r_i][c_i] == Element.BOULDER:
                            positions.append((r_i, c_i))
            elif direction == Direction.WEST or direction == Direction.EAST:
                cols = range(1, col_n) if direction == Direction.WEST else range(col_n - 2, -1, -1)
                for r_i in range(self.content.shape[0]):
                    for c_i in cols:
                        if self.content[r_i][c_i] == Element.BOULDER:
                            positions.append((r_i, c_i))
            yield positions
        finally:
            pass

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(
                self._map_from_element(element) for element in line)
            for line in self.content
        )

    def get_load(self) -> int:
        load = 0
        rows, cols = self.content.shape
        for r_i in range(rows):
            for c_i in range(cols):
                if self.content[r_i][c_i] == Element.BOULDER:
                    load += rows - r_i
        return load

    def tilt(self, direction: Direction = Direction.NORTH) -> None:
        with self.boulder_positions(direction) as positions:
            for r_i, c_i in positions:
                self._move_boulder_up(r_i, c_i)

    def _move_boulder_up(self, row: int, column: int) -> None:
        if row == 0 or self.content[row - 1][column] != Element.SPACE:
            return
        self.content[row][column] = Element.SPACE
        self.content[row - 1][column] = Element.BOULDER
        self._move_boulder_up(row - 1, column)


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
