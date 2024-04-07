#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/4

Usage: solution.py
"""


import math
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Race:
    """Store information about a race"""

    time: int
    distance: int


class Speedboat:
    """Loads in a scratch card number with its solution"""

    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text("utf-8").strip().split("\n")
        times = list(file_contents[0].split()[1:])
        distances = list(file_contents[1].split()[1:])
        self.races = [
            Race(time=int(time), distance=int(distance))
            for (time, distance) in zip(times, distances)
        ]
        self.race = Race(distance=int("".join(distances)), time=int("".join(times)))

    def get_winning_product(self) -> int:
        """Return product of winning possibility sum."""
        ret_val = 1
        for race in self.races:
            ret_val *= self._get_winning_num(race)
        if ret_val == 1:
            ret_val = 0
        return ret_val

    def get_winning_num(self) -> int:
        """Returns the winning possibility sum for massive race."""
        return self._get_winning_num(self.race)

    def _get_winning_num(self, race: Race) -> int:
        """
        d = distance, t = time, c = charge time, v = velocity
        v = c .......... (1)
        d = (t - c) v
          = t.c - c^2 .. (2)
        ∴ c^2 - t.c + d = 0
        c = (t +- (t^2 - 4.d)^0.5) / 2
        Where c will result in the two values that will result in a draw. Natural numbers between
        c1 and c2 will win the race.
        """
        t = race.time
        d = race.distance
        lower_bound = max((t - (t**2 - 4 * d) ** 0.5) / 2, 0)
        lower_bound = lower_bound + 1 if lower_bound.is_integer() else math.ceil(lower_bound)
        upper_bound = min((t + (t**2 - 4 * d) ** 0.5) / 2, t)
        upper_bound = upper_bound - 1 if upper_bound.is_integer() else math.floor(upper_bound)
        return upper_bound - lower_bound + 1


if __name__ == "__main__":
    assert Speedboat("example.txt").get_winning_product() == 288

    puzzle_result = Speedboat("puzzle_input.txt")
    print(f"The product of the winning sums for puzzle 01: {puzzle_result.get_winning_product()}")
    print(f"The winning sums for puzzle 02: {puzzle_result.get_winning_num()}")
