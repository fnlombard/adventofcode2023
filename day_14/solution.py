#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/14

Usage: solution.py
"""

from contextlib import contextmanager
from enum import Enum, auto
from pathlib import Path
from typing import Iterator, List, Optional, Tuple

import numpy as np


class Element(Enum):
    SPACE = auto()
    CUBE = auto()
    BOULDER = auto()


class Board:
    def __init__(self, board_data: List[str]) -> None:
        self.content = np.array([
            [self._map_to_element(character) for character in line]
            for line in board_data
        ])

    def _map_to_element(self, character: str) -> Element:
        if character == '.':
            return Element.SPACE
        elif character == 'O':
            return Element.BOULDER
        elif character == '#':
            return Element.CUBE
        else:
            raise RuntimeError(f"Unkown character: {character}")

    def _map_from_element(self, element: Element) -> str:
        if element == Element.BOULDER:
            return "O"
        elif element == Element.CUBE:
            return "#"
        elif element == Element.SPACE:
            return "."
        else:
            raise RuntimeError(f"Unkown element: {element}")

    @contextmanager
    def boulder_positions(self) -> Iterator[List[Tuple[int, int]]]:
        try:
            positions = []
            row_n, col_n = self.content.shape
            for c_i in range(col_n):
                for r_i in range(1, row_n):
                    if self.content[r_i][c_i] == Element.BOULDER:
                        positions.append((r_i, c_i))
            yield positions
        finally:
            pass

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(
                self._map_from_element(element) for element in line)
            for line in self.content
        )

    def get_load(self) -> int:
        load = 0
        rows, cols = self.content.shape
        for r_i in range(rows):
            for c_i in range(cols):
                if self.content[r_i][c_i] == Element.BOULDER:
                    load += rows - r_i
        return load

    def spin_cycle(self) -> None:
        for _ in range(4):
            self.tilt_north()
            self.content = np.rot90(self.content, 3)  # 3 for counter-clockwise

    def load_after_n_cycles(self, n_cycles: int) -> int:
        if not isinstance(n_cycles, int):
            n_cycles = int(n_cycles)

        load_values = np.array([self.get_load()])
        for _ in range(n_cycles):
            self.spin_cycle()
            load_values = np.append(load_values, self.get_load())
            if len(load_values) > 1e3:
                oscillation_period = self._oscillation_period(load_values)
                if oscillation_period is not None:
                    pattern = load_values[-oscillation_period:]
                    pattern_idx = (n_cycles - len(load_values)) % len(pattern)
                    return pattern[pattern_idx]
        return self.get_load()

    def _oscillation_period(self, data: np.ndarray, threshold: int = 0.01) -> Optional[int]:
        data_without_dc = data - np.mean(data)
        windowed_data = data_without_dc * np.hanning(len(data_without_dc))
        fft_result = np.fft.fft(windowed_data)
        frequencies = np.fft.fftfreq(len(data), d=1.0)  # Unit time interval
        magnitude = np.abs(fft_result)

        ignore_freq_below = threshold
        magnitude[frequencies < ignore_freq_below] = 0
        dominant_freq_idx = np.argmax(magnitude)
        dominant_frequency = frequencies[dominant_freq_idx]
        if dominant_frequency == 0:
            return None
        period = round(1 / dominant_frequency)

        if period < len(data) // 10:  # Ensure you get all frequencies
            return period
        return None

    def tilt_north(self) -> None:
        with self.boulder_positions() as positions:
            for r_i, c_i in positions:
                self._move_boulder_north(r_i, c_i)

    def _move_boulder_north(self, row: int, column: int) -> None:
        while row > 0 and self.content[row - 1][column] == Element.SPACE:
            self.content[row][column] = Element.SPACE
            row -= 1
            self.content[row][column] = Element.BOULDER


class Solution:
    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text('utf-8').strip().split('\n')
        self.board = Board(board_data=file_contents)

    def puzzle_01(self) -> int:
        self.board.tilt_north()
        return self.board.get_load()

    def puzzle_02(self) -> int:
        return self.board.load_after_n_cycles(1e9)


if __name__ == '__main__':
    assert Solution("example.txt").puzzle_01() == 136
    assert Solution("example.txt").puzzle_02() == 64

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.puzzle_01()}")
    print(f"Solution 01: {puzzle_result.puzzle_02()}")
