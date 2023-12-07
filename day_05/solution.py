#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/4

Usage: solution.py
"""


from pathlib import Path
from typing import List


class Almanac:
    """Loads in a scratch card number with its solution"""

    def __init__(self, filename: str) -> None:
        self.lines: List[str] = Path(filename).read_text('utf-8').strip().split('\n')

    def lowest_location_number(self) -> int:
        """Returns the lowest location number"""
        return 0


if __name__ == '__main__':
    assert Almanac("example_01.txt").lowest_location_number() == 35
