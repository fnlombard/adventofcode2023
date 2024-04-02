#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/16

Usage: solution.py
"""

from pathlib import Path


class EnergiseGrid:
    def __init__(self, definition: str) -> None: ...

    def get_energised_tiles(self) -> int:
        return 1


class Solution:
    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text("utf-8").strip().split("\n")[0]
        self.energised_grid = EnergiseGrid(definition=file_contents)

    def puzzle_01(self) -> int:
        return self.energised_grid.get_energised_tiles()

    def puzzle_02(self) -> int:
        return 0


if __name__ == "__main__":
    assert Solution("example.txt").puzzle_01() == 46
    # assert Solution("example.txt").puzzle_02() == 145

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.puzzle_01()}")
    # print(f"Solution 02: {puzzle_result.puzzle_02()}")
