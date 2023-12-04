#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/1

Usage: solution.py input_file
"""
from pathlib import Path
from typing import Optional
import argparse
import cProfile
import re


def _parse_args() -> Optional[Path]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        required=True)
    (args, _) = parser.parse_known_args()

    file_path = Path(args.file)
    if not file_path:
        return None

    if not file_path.exists():
        file_path = Path.cwd() / file_path

    if not file_path.exists() or not file_path.is_file():
        return None

    return file_path

value_map = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

valid_keys = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

REGEX_GROUP = f'{"|".join(valid_keys)}'
REGEX_FIRST = f'({REGEX_GROUP}).*'
REGEX_LAST = f'({REGEX_GROUP[::-1]}).*'


def _get_elf_number(line: str) -> int:
    """To deal with overlaps, parse from the front and the back."""
    match_first = re.search(REGEX_FIRST, line)

    if not match_first:
        return 0

    first_digit = match_first.group(1)
    match_second = re.search(REGEX_LAST, line[::-1])
    last_digit = match_second.group(1)[::-1] if match_second else first_digit

    return int(value_map[first_digit] + value_map[last_digit])


def main():
    input_file_path = _parse_args()
    if not input_file_path:
        print("File does not exist")

    elf_sum = 0
    with open(input_file_path) as file:
        for line in file:
            elf_sum += _get_elf_number(line)

    print(elf_sum)


if __name__ == '__main__':
    cProfile.run('main()')