#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/4

Usage: solution.py
"""


from enum import Enum
from pathlib import Path
import re
from typing import Dict, List, Tuple
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

    def __repr__(self) -> str:
        return f"{self.source_range_start}-{self.desintation_range_start}-{self.range_length}"


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
                    range_length=int(value_range),
                )
            )
        self._maps.sort(key=lambda item: item.source_range_start)

    def map_value(self, source_value: float) -> Tuple[float, float]:
        """Returns mapped value"""
        destination_value = source_value
        range_to_end = float(1)

        for index, map_info in enumerate(self._maps):
            if source_value < map_info.source_range_start:
                range_to_end = self._maps[index].source_range_start - source_value
                break

            if (
                map_info.source_range_start
                <= source_value
                < map_info.source_range_start + map_info.range_length
            ):
                destination_value = (
                    map_info.desintation_range_start + source_value - map_info.source_range_start
                )
                range_to_end = map_info.range_length - (map_info.source_range_start - source_value)
                range_to_end /= 2
                break

            if (
                index + 1 < len(self._maps)
                and source_value < self._maps[index + 1].source_range_start
            ):
                destination_value = source_value
                range_to_end = self._maps[index + 1].source_range_start - source_value
                break

        return (destination_value, range_to_end)

    def __repr__(self) -> str:
        ret_val = ""
        for range_map in self._maps:
            ret_val += f"{range_map.desintation_range_start} "
            ret_val += f"{range_map.source_range_start} "
            ret_val += f"{range_map.range_length}\n"
        return ret_val


class Almanac:
    """Loads in a scratch card number with its solution"""

    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text("utf-8").strip().split("\n\n")
        self.seeds = [int(seed) for seed in file_contents.pop(0).split(":")[1].split()]
        self._range_maps: Dict[str, RangeMap] = {}
        for chunk in file_contents:
            data = chunk.split("\n")
            match = re.search(r"(\w+-to-\w+) map:", data.pop(0))
            if match is None:
                raise ValueError("Expected a regex hit; expected input of different format.")
            key = match.group(1)
            self._range_maps[key] = RangeMap(data)

    def lowest_location_number(self) -> int:
        """Returns the lowest location number"""
        min_location = float("inf")
        for seed in self.seeds:
            test_value, _ = self._calculate_location_and_range(seed)
            min_location = min(min_location, test_value)
        return int(min_location)

    def lowest_location_number_in_range(self) -> int:
        """Returns the lowest location number in seed range"""
        min_location = float("inf")
        seed_ranges = list(zip(self.seeds[::2], self.seeds[1::2]))
        seed_ranges.sort(key=lambda value: value[0])
        for seed_start, seed_range in seed_ranges:
            seed = float(seed_start)
            while seed < seed_start + seed_range:
                print(seed)
                (test_location, test_range) = self._calculate_location_and_range(seed)
                min_location = min(min_location, test_location)
                seed += test_range
        return int(min_location)

    def _calculate_location_and_range(self, seed: float) -> Tuple[float, float]:
        stages = [
            "seed-to-soil",
            "soil-to-fertilizer",
            "fertilizer-to-water",
            "water-to-light",
            "light-to-temperature",
            "temperature-to-humidity",
            "humidity-to-location",
        ]
        min_range = float("inf")
        for stage in stages:
            (seed, map_range) = self._range_maps[stage].map_value(seed)
            min_range = min(min_range, map_range)
        return (seed, min_range)


if __name__ == "__main__":
    assert Almanac("example.txt").lowest_location_number() == 35
    assert Almanac("example.txt").lowest_location_number_in_range() == 46

    puzzle_result = Almanac("puzzle_input.txt")
    print(f"Lowest location value for puzzle 01: {puzzle_result.lowest_location_number()}")
    print(
        f"Lowest location value in seed range for puzzle 02: "
        f"{puzzle_result.lowest_location_number_in_range()}"
    )
