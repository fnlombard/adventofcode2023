#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/4

Usage: solution.py
"""


from pathlib import Path
import re
from typing import List, Literal


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
            print(seed)
            print(f'{soil}-{fertilizer}-{water}-{light}-{temperature}-{humidity}-{location}')
            if location < lowest_value:
                lowest_value = location
        print(lowest_value)
        return lowest_value

    def _map_value(self, from_type: str, to_type: str, value: int) -> int:
        for chunk in self.chunks:
            lines = chunk.split('\n')
            if not lines.pop(0).startswith(f'{from_type}-to-{to_type}'):
                continue
            for line in lines:
                values = line.split()
                source_start = int(values[0])
                destination_start = int(values[1])
                value_range = int(values[2])

                if source_start <= value <= source_start + value_range:
                    return source_start - destination_start + value
        return value


if __name__ == '__main__':
    assert Almanac("example_01.txt").lowest_location_number() == 35
