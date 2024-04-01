#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/2

Usage: solution.py
"""

import math
from pathlib import Path
import re
from typing import Literal


class Cubes:
    """Reads file containing game information and computes elf madness"""

    def __init__(self, filename) -> None:
        self.lines = Path(filename).read_text("utf-8").strip().split("\n")

    def get_possible_games_id_sum(
        self, red_cubes: int, green_cubes: int, blue_cubes: int
    ) -> int:
        """Returns sum of possible game IDs"""
        id_sum = 0
        for line in self.lines:
            if self._is_game_valid(line, red_cubes, green_cubes, blue_cubes):
                id_sum += self._get_game_id(line)

        return id_sum

    def _is_game_valid(self, line: str, red: int, green: int, blue: int) -> bool:
        for game_set in line.split(";"):
            if (
                self._get_red(game_set) > red
                or self._get_green(game_set) > green
                or self._get_blue(game_set) > blue
            ):
                return False
        return True

    def get_power_cubes(self) -> int:
        """Returns power cubes"""
        power_cubes = 0
        for line in self.lines:
            rgb_max = [0, 0, 0]
            for game_set in line.split(";"):
                rgb_set = [
                    self._get_red(game_set),
                    self._get_green(game_set),
                    self._get_blue(game_set),
                ]
                rgb_max = [max(rgb_max[i], rgb_set[i]) for i in range(3)]
            power_cubes += math.prod(rgb_max)
        return power_cubes

    def _get_game_id(self, raw: str) -> int:
        match = re.search(r"Game (\d+):", raw)

        if not match:
            raise RuntimeError(f"Cannot parse Game ID from {raw}")

        return int(match.group(1))

    def _get_red(self, raw: str) -> int:
        return self._get_colour(raw, "red")

    def _get_green(self, raw: str) -> int:
        return self._get_colour(raw, "green")

    def _get_blue(self, raw: str) -> int:
        return self._get_colour(raw, "blue")

    def _get_colour(self, raw: str, colour: Literal["red", "green", "blue"]) -> int:
        match = re.search(f"(\\d+) {colour}", raw)
        if not match:
            return 0

        return int(match.group(1))


if __name__ == "__main__":
    assert Cubes("example_01.txt").get_possible_games_id_sum(12, 13, 14) == 8
    assert Cubes("example_02.txt").get_power_cubes() == 2286

    puzzle_result = Cubes("puzzle_input.txt")
    print(
        f"ID sum for puzzle 01: {puzzle_result.get_possible_games_id_sum(12, 13, 14)}"
    )
    print(f"Power cubes for puzzle 01: {puzzle_result.get_power_cubes()}")
