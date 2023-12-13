#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/13

Usage: solution.py
"""


from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List


class Direction(Enum):
    Vertical = auto()
    Horizontal = auto()


@dataclass
class Reflection:
    direction: Direction


@dataclass
class HorizontalReflection(Reflection):
    direction = Direction.Horizontal
    rows_above: int


@dataclass
class VerticalReflection(Reflection):
    direction = Direction.Vertical
    colums_left: int


class MirrorMaze:
    """Loads in the Mirror Maze and processes it."""

    def __init__(self, filename: str) -> None:
        file_content: List[str] = Path(filename).read_text('utf-8').strip().split('\n\n')


if __name__ == '__main__':
    ...
    # assert SpringMap("example.txt").get_winning_pot() == 21
