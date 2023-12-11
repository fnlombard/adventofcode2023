#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/4

Usage: solution.py
"""


from enum import Enum
from pathlib import Path
import re
from typing import Dict, List
from dataclasses import dataclass


class MapOption(Enum):
    """Map options"""
    SEED_2_SOIL = "seed-to-soil"
    SOIL_2_FERTILIZER = "soil-to-fertilizer"
    FERTILIZER_2_WATER = "fertilizer-to-water"
    WATER_2_LIGHT = "water-to-light"
    LIGHT_2_TEMPERATURE = "light-to-temperature"
    TEMPERATURE_2_HUMIDITY = "temperature-to-humidity"
    HUMIDITY_2_LOCATION = "humidity-to-location"


@dataclass
class MapInformation:
    """Map information"""
    desintation_range_start: int
    source_range_start: int
    range_length: int


class RangeMap:
    """Store map in memory for quicker access"""

    def __init__(self, lines: List[str]) -> None:
        self._maps: List[MapInformation] = []
        for line in lines:
            (destination, source, value_range) = line.split()
            self._maps.append(
                MapInformation(
                    source_range_start=int(source),
                    desintation_range_start=int(destination),
                    range_length=int(value_range))
            )
        self._maps.sort(key=lambda item: item.source_range_start)

    def map_value(self, value: int) -> int:
        """Returns mapped value"""
        for index, map_info in enumerate(self._maps):
            if map_info.source_range_start <= value < map_info.source_range_start + map_info.range_length:
                return map_info.desintation_range_start + value - map_info.source_range_start
            elif index + 1 < len(self._maps) and value < self._maps[index + 1].source_range_start:
                return value
        return value

    def __repr__(self) -> str:
        ret_val = ""
        for map in self._maps:
            ret_val += f"{map.desintation_range_start} {map.source_range_start} {map.range_length}\n"
        return ret_val


class Almanac:
    """Loads in a scratch card number with its solution"""

    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text('utf-8').strip().split('\n\n')
        self.seeds = [int(seed) for seed in file_contents.pop(0).split(':')[1].split()]
        # self.chunks = {}
        self._range_maps: Dict[str, RangeMap] = {}
        for chunk in file_contents:
            data = chunk.split('\n')
            match = re.search(r'(\w+-to-\w+) map:', data.pop(0))
            key = match.group(1)
            self._range_maps[key] = RangeMap(data)
            # self.chunks[data[0]] = data[1:]

    def lowest_location_number(self) -> int:
        """Returns the lowest location number"""
        min_location = float('inf')
        for seed in self.seeds:
            test_value = self._calculate_location(seed)
            if test_value < min_location:
                min_location = test_value
        return min_location

    def lowest_location_number_in_range(self) -> int:
        """Returns the lowest location number in seed range"""
        min_location = float('inf')
        for seed_start, seed_range in zip(self.seeds[::2], self.seeds[1::2]):
            for seed in range(seed_start, seed_start + seed_range):
                test_location = self._calculate_location(seed)
                if test_location < min_location:
                    min_location = test_location
        return min_location

    def _calculate_location(self, seed: int) -> int:
        stages = [
            "seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature", "temperature-to-humidity", "humidity-to-location"
        ]
        for stage in stages:
            seed = self._range_maps[stage].map_value(seed)
        return seed


if __name__ == '__main__':
    assert Almanac("example.txt").lowest_location_number() == 35
    assert Almanac("example.txt").lowest_location_number_in_range() == 46

    puzzle_result = Almanac("puzzle_input.txt")
    print(f"Lowest location value for puzzle 01: {puzzle_result.lowest_location_number()}")
    print(f"Lowest location value in seed range for puzzle 01: {puzzle_result.lowest_location_number_in_range()}")
