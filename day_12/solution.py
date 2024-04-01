#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/12

Usage: solution.py
"""


from pathlib import Path
from typing import List


class SpringMap:
    """Loads in broken spring map and processes it."""

    def __init__(self, filename: str) -> None:
        self.lines: List[str] = Path(filename).read_text("utf-8").strip().split("\n")

    def get_sum_of_broken_spring_variance(self) -> int:
        for line in self.lines:
            (record, contiguous_groups) = line.split()
            groups = [int(group) for group in contiguous_groups]
        return 0


if __name__ == "__main__":
    # assert SpringMap("example.txt").get_winning_pot() == 21
    pass
