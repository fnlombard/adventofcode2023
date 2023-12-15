#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/14

Usage: solution.py
"""

from enum import Enum, auto
from pathlib import Path
from typing import List


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


class Board:
    def __init__(self, board_data: List[str]) -> None:
        pass

    def get_load(self) -> int: ...

    def tilt(self, direction: Direction = Direction.NORTH) -> None: ...


class Solution:
    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text('utf-8').strip().split('\n\n')
        self.board = Board(board_data=file_contents)

    def puzzle_01(self) -> int:
        return self.board.get_load()


if __name__ == '__main__':
    assert Solution("example.txt").puzzle_01() == 136

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.puzzle_01()}")
