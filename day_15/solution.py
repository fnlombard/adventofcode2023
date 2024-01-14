#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/15

Usage: solution.py
"""

from contextlib import contextmanager
from enum import Enum, auto
from pathlib import Path
from typing import Iterator, List, Optional, Tuple
from functools import reduce


class AsciiParser:
    def __init__(self, ascii_string: str) -> None:
        self.ascii_string_ = ascii_string

    def _get_value(self, ascii: str) -> int:
        calculate_ascii_value = (
            lambda first_char, second_char: (first_char + second_char) * 17 % 256
        )
        return reduce(calculate_ascii_value, [0] + [ord(char) for char in ascii])

    def get_total_value(self) -> int:
        return sum([self._get_value(ascii) for ascii in self.ascii_string_.split(",")])


class Solution:
    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text("utf-8").strip().split("\n")[0]
        self.ascii_parser_ = AsciiParser(ascii_string=file_contents)

    def puzzle_01(self) -> int:
        return self.ascii_parser_.get_total_value()

    def puzzle_02(self) -> int:
        return 0


if __name__ == "__main__":
    assert Solution("example.txt").puzzle_01() == 1320
    # assert Solution("example.txt").puzzle_02() == 64

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.puzzle_01()}")
    print(f"Solution 02: {puzzle_result.puzzle_02()}")
