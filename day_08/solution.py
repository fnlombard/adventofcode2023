#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/8

Usage: solution.py
"""

from pathlib import Path
import re
from typing import Dict


def get_number_lookups(input_path: Path) -> int:
    directions, _, *node_maps = input_path.read_text(encoding="utf-8").split("\n")

    pattern = r"(\w+) = \((\w+), (\w+)\)"
    mappings: Dict[str, Dict[str, str]] = {}
    for node_map in node_maps:
        matches = re.match(pattern, node_map)
        assert matches

        key, left, right = matches.groups()
        mappings[key] = {
            "L": left,
            "R": right,
        }

    current_position = "AAA"
    destination = "ZZZ"

    lookups = 0
    while True:
        for direction in directions:
            current_position = mappings[current_position][direction]
            lookups += 1
            if current_position == destination:
                return lookups


if __name__ == "__main__":
    assert get_number_lookups(Path("example.txt")) == 6

    puzzle_input = Path("puzzle_input.txt")
    print(f"Steps required for puzzle 01: {get_number_lookups(puzzle_input)}")
    print(f"The winning sums for puzzle 02: {puzzle_result.get_winning_num()}")
