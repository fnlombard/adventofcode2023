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
        self.chunks: List[str] = Path(filename).read_text('utf-8').strip().split('\n\n')
        self.seeds = [
            int(seed)
            for seed in self.chunks.pop(0).split(':')[1].split()
        ]

    def lowest_location_number(self) -> int:
        """Returns the lowest location number"""
        lowest_value = float('inf')
        for seed in self.seeds:
            soil = self._map_value("seed", "soil", seed)
            fertilizer = self._map_value("soil", "fertilizer", soil)
            water = self._map_value("fertilizer", "water", fertilizer)
            light = self._map_value("water", "light", water)
            temperature = self._map_value("light", "temperature", light)
            humidity = self._map_value("temperature", "humidity", temperature)
            location = self._map_value("humidity", "location", humidity)
            if location < lowest_value:
                lowest_value = location
        return lowest_value

    def _map_value(self, from_type: str, to_type: str, value: int) -> int:
        for chunk in self.chunks:
            lines = chunk.split('\n')
            if not lines.pop(0).startswith(f'{from_type}-to-{to_type}'):
                continue
            for line in lines:
                values = line.split()
                destination_start = int(values[0])
                source_start = int(values[1])
                value_range = int(values[2])

                if source_start <= value <= source_start + value_range:
                    return destination_start + value - source_start
        return value


if __name__ == '__main__':
    assert Almanac("example_01.txt").lowest_location_number() == 35

    puzzle_result = Almanac("puzzle_input.txt")
    print(f"Lowest Location value for puzzle 01: {puzzle_result.lowest_location_number()}")
