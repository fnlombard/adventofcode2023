#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/13

Usage: solution.py
"""

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List

import numpy as np


class Direction(Enum):
    """Describes matrix reflection orientation"""
    VERTICAL = auto()
    HORIZONTAL = auto()
    UNKNOWN = auto()


@dataclass
class MatrixSignature:
    """Used to compare relfection matrices"""
    reflection_line: int
    reflection_size: int


class MirrorMaze:
    """Contains maze information"""

    def __init__(self, raw_maze: List[str]) -> None:
        if not raw_maze:
            raise ValueError("raw_maze cannot be empty")

        row_length = len(raw_maze[0])
        maze_list = []
        for line in raw_maze:
            if len(line) != row_length:
                raise RuntimeError("Inconsistent row lengths in the maze")
            maze_list.append([self._char_to_int(char) for char in line])

        self.maze = np.array(maze_list)

    def _char_to_int(self, char: str) -> int:
        if char == ".":
            return 0
        elif char == "#":
            return 1
        else:
            raise RuntimeError(f"Unexpected character: {char}")

    def get_reflection_checksum(self, tolerance: int) -> int:
        """Get reflection checksum for the matrix"""

        reflect_signature_vert, size_vert = self._get_submatrix_signature(self.maze, tolerance)

        self.maze = np.rot90(self.maze)
        reflect_signature_hor, size_hor = self._get_submatrix_signature(self.maze, tolerance)

        if reflect_signature_vert == reflect_signature_hor == -1:
            raise RuntimeError(f"No reflection found for matrix:\n{self.maze}")

        if size_vert > size_hor:
            return reflect_signature_vert
        else:
            return reflect_signature_hor * 100

    def _get_submatrix_signature(self, matrix: np.ndarray, tolerance) -> (int, int):
        columns = matrix.shape[1]
        max_window_size = columns if columns % 2 == 0 else columns - 1
        min_window_size = 2

        for window_size in range(max_window_size, min_window_size - 1, -2):
            # Must only test beginning and end:
            submatrix = matrix[:, :window_size]
            if self._is_matrix_symmetric(submatrix, tolerance):
                return window_size // 2, window_size
            submatrix = matrix[:, -window_size:]
            if self._is_matrix_symmetric(submatrix, tolerance):
                return columns - window_size // 2, window_size
        return -1, -1

    def _is_matrix_symmetric(self, matrix: np.ndarray, tolerance) -> bool:
        columns = matrix.shape[1]
        if columns % 2 != 0:
            raise RuntimeError("Cannot determine if matrix of uneven columns are vertically semitrical.")
        left = matrix[:, columns // 2:]
        right = np.fliplr(matrix[:, :columns // 2])
        return np.count_nonzero(np.absolute((np.subtract(left, right))) == 1) == tolerance


class Solution:
    """Loads in the Mirror Maze and processes it."""

    def __init__(self, filename: str) -> None:
        file_contents: List[str] = Path(filename).read_text('utf-8').strip().split('\n\n')
        self.mazes: List[MirrorMaze] = []
        for content in file_contents:
            self.mazes.append(MirrorMaze(content.split()))

    def get_maze_checksum(self, tolerance: int = 0) -> int:
        """Solution for puzzle 01"""
        checksum = 0
        for index, maze in enumerate(self.mazes):
            test = maze.get_reflection_checksum(tolerance)
            checksum += test
        return checksum


if __name__ == '__main__':
    assert Solution("example.txt").get_maze_checksum() == 405
    assert Solution("example.txt").get_maze_checksum(tolerance=1) == 400

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.get_maze_checksum()}")
    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 02: {puzzle_result.get_maze_checksum(tolerance=1)}")
