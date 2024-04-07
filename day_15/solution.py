#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/15

Usage: solution.py
"""

from pathlib import Path
from typing import List, Optional
from functools import reduce
from dataclasses import dataclass


@dataclass
class Lens:
    label: str
    focal_length: int


class Box:
    def __init__(self) -> None:
        self.lenses: List[Lens] = []

    def add_lens(self, lens: Lens) -> None:
        if (lens_index := self.contains_lens_(lens.label)) is not None:
            self.lenses[lens_index].focal_length = lens.focal_length
        else:
            self.lenses.append(lens)

    def remove_lens(self, label: str) -> None:
        self.lenses = [lens for lens in self.lenses if lens.label != label]

    def contains_lens_(self, label: str) -> Optional[int]:
        for index, lens in enumerate(self.lenses):
            if lens.label == label:
                return index
        return None


class AsciiParser:
    def __init__(self, ascii_string: str) -> None:
        self.ascii_string_ = ascii_string
        self.boxes_: List[Box] = [Box() for _ in range(256)]

    def _get_value(self, tmp_ascii: str) -> int:
        calculate_ascii_value = (
            lambda first_char, second_char: (first_char + second_char) * 17 % 256
        )

        return reduce(calculate_ascii_value, [ord(char) for char in tmp_ascii], 0)

    def get_total_value(self) -> int:
        return sum([self._get_value(ascii) for ascii in self.ascii_string_.split(",")])

    def get_focussing_power(self) -> int:
        for ascii_string in self.ascii_string_.split(","):
            if "=" in ascii_string:
                label, focal_length = ascii_string.split("=")
                self.boxes_[self._get_value(label)].add_lens(Lens(label, int(focal_length)))
            elif "-" in ascii_string:
                label, _ = ascii_string.split("-")
                self.boxes_[self._get_value(label)].remove_lens(label)
            else:
                raise Exception(f"Unexpected value: {ascii_string}")

        return sum(
            [
                (box_num + 1) * (lens_num + 1) * lens.focal_length
                for box_num, box in enumerate(self.boxes_)
                for lens_num, lens in enumerate(box.lenses)
            ]
        )


class Solution:
    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text("utf-8").strip().split("\n")[0]
        self.ascii_parser_ = AsciiParser(ascii_string=file_contents)

    def puzzle_01(self) -> int:
        return self.ascii_parser_.get_total_value()

    def puzzle_02(self) -> int:
        return self.ascii_parser_.get_focussing_power()


if __name__ == "__main__":
    assert Solution("example.txt").puzzle_01() == 1320
    assert Solution("example.txt").puzzle_02() == 145

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.puzzle_01()}")
    print(f"Solution 02: {puzzle_result.puzzle_02()}")
