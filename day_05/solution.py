#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/4

Usage: solution.py
"""


from pathlib import Path
from typing import Dict, Tuple


class Almanac:
    """Loads in a scratch card number with its solution"""

    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text('utf-8').strip().split('\n\n')
        self.seeds = [int(seed) for seed in file_contents.pop(0).split(':')[1].split()]
        self.chunks = {}
        for chunk in file_contents:
            data = chunk.split('\n')
            self.chunks[data[0]] = data[1:]
        self.mapping_cache: Dict[Tuple[str, str, int], int] = {}

    def lowest_location_number(self) -> int:
        """Returns the lowest location number"""
        return min(self._calculate_location(seed) for seed in self.seeds)

    def lowest_location_number_in_range(self) -> int:
        """Returns the lowest location number in seed range"""
        locations = []
        for seed_start, seed_range in zip(self.seeds[::2], self.seeds[1::2]):
            for seed in range(seed_start, seed_start + seed_range):
                print(f'current seed: {seed}')
                locations.append(self._calculate_location(seed))
        return min(locations)

    def _calculate_location(self, seed: int) -> int:
        stages = [
            "seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"
        ]
        for i in range(len(stages) - 1):
            seed = self._map_value(stages[i], stages[i + 1], seed)
        return seed

    def _map_value(self, from_type: str, to_type: str, value: int) -> int:
        if (from_type, to_type, value) in self.mapping_cache:
            return self.mapping_cache[(from_type, to_type, value)]
        for line in self.chunks.get(f'{from_type}-to-{to_type} map:', []):
            dest_start, source_start, value_range = map(int, line.split())
            if source_start <= value <= source_start + value_range:
                result = dest_start + value - source_start
                self.mapping_cache[(from_type, to_type, value)] = result
                return result

        self.mapping_cache[(from_type, to_type, value)] = value
        return value


if __name__ == '__main__':
    assert Almanac("example.txt").lowest_location_number() == 35
    assert Almanac("example.txt").lowest_location_number_in_range() == 46

    puzzle_result = Almanac("puzzle_input.txt")
    print(f"Lowest location value for puzzle 01: {puzzle_result.lowest_location_number()}")
    print(f"Lowest location value in seed range for puzzle 01: {puzzle_result.lowest_location_number_in_range()}")
