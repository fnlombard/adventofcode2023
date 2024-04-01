#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/3

Usage: solution.py
"""

from pathlib import Path
import re
from typing import List

# Must read from East to West
DIRECTIONS = [
    [-1, 1],  # NE
    [-1, 0],  # N
    [-1, -1],  # NW
    [0, 1],  # E
    [0, -1],  # W
    [1, 1],  # SE
    [1, 0],  # S
    [1, -1],  # SW
]


class Engine:
    """Reads file engine schematic and processes it."""

    def __init__(self, filename) -> None:
        self.lines: List[str] = Path(filename).read_text("utf-8").strip().split("\n")

    def get_part_number_sum(self) -> int:
        """Returns part number sum"""

        ret_val = 0
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                if not char.isalnum() and char != ".":
                    ret_val += self._get_surrounding_sum(x, y)
        return ret_val

    def get_gear_ratio(self) -> int:
        """Returns the gear ratio. Bad solution - It will not work for overlapping gears."""
        ret_val = 0
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                if not char.isalnum() and char != ".":
                    ret_val += self._get_surrounding_product(x, y)
        return ret_val

    def _get_and_replace_number(self, x: int, y: int) -> int:
        """Search East and grab from West."""
        extend_search = 0
        for character in self.lines[y][x + 1 :]:
            if character.isdigit():
                extend_search += 1
            else:
                break

        match = re.search(r"(\d+)$", self.lines[y][: x + extend_search + 1])
        assert match

        (start, end) = match.span()
        self.lines[y] = (
            self.lines[y][:start] + "." * (end - start) + self.lines[y][end:]
        )
        return int(match.group(1))

    def _get_surrounding_sum(self, x: int, y: int) -> int:
        ret_val = 0
        for dy, dx in DIRECTIONS:
            ye = self._clamp(y + dy, len(self.lines))
            xe = self._clamp(x + dx, len(self.lines[ye]))
            if self.lines[ye][xe].isdigit():
                ret_val += self._get_and_replace_number(xe, ye)

        return ret_val

    def _get_surrounding_product(self, x: int, y: int) -> int:
        counter = 0
        ret_val = 1
        for dy, dx in DIRECTIONS:
            ye = self._clamp(y + dy, len(self.lines))
            xe = self._clamp(x + dx, len(self.lines[ye]))
            if self.lines[ye][xe].isdigit():
                ret_val *= self._get_and_replace_number(xe, ye)
                counter += 1
        if counter != 2:
            return 0

        return ret_val

    def _clamp(self, value: int, upper_bound: int, lower_bound: int = 0) -> int:
        return min(max(value, lower_bound), upper_bound)


if __name__ == "__main__":
    assert Engine("example_01.txt").get_part_number_sum() == 4361
    assert Engine("example_02.txt").get_gear_ratio() == 467835

    puzzle_result = Engine("puzzle_input.txt")
    print(f"Part number sum for puzzle 01: {puzzle_result.get_part_number_sum()}")
    puzzle_result = Engine("puzzle_input.txt")
    print(f"Gear ratio sum for puzzle 02: {puzzle_result.get_gear_ratio()}")
