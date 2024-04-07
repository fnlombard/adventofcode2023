#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/13

Usage: solution.py
"""
# pylint: disable=too-few-public-methods

from enum import Enum, auto
from pathlib import Path
from typing import List, NamedTuple
import numpy as np


class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()
    UNKNOWN = auto()


class MatrixSignature(NamedTuple):
    reflection_line: int
    reflection_size: int


class MirrorMaze:
    def __init__(self, raw_maze: List[str]) -> None:
        if not raw_maze:
            raise ValueError("raw_maze cannot be empty")

        self.maze = np.array([[1 if char == "#" else 0 for char in line] for line in raw_maze])

    def get_reflection_checksum(self, tolerance: int) -> int:
        vert_sig = self._get_submatrix_signature(self.maze, tolerance)
        hor_sig = self._get_submatrix_signature(np.rot90(self.maze), tolerance)

        if vert_sig.reflection_line == hor_sig.reflection_line == -1:
            raise RuntimeError(f"No reflection found for matrix:\n{self.maze}")

        return max(vert_sig.reflection_line, hor_sig.reflection_line * 100)

    def _get_submatrix_signature(self, matrix: np.ndarray, tolerance) -> MatrixSignature:
        columns = matrix.shape[1]
        max_window_size = columns - (columns % 2)

        for window_size in range(max_window_size, 1, -2):
            if self._is_matrix_symmetric(matrix[:, :window_size], tolerance):
                return MatrixSignature(window_size // 2, window_size)
            if self._is_matrix_symmetric(matrix[:, -window_size:], tolerance):
                return MatrixSignature(columns - window_size // 2, window_size)
        return MatrixSignature(-1, -1)

    def _is_matrix_symmetric(self, matrix: np.ndarray, tolerance) -> bool:
        # Splitting the matrix in twine results in a balanced tuple unpacking.
        # pylint: disable-next=unbalanced-tuple-unpacking
        left, right = np.split(matrix, 2, axis=1)
        return np.count_nonzero(left != np.fliplr(right)) == tolerance


class Solution:
    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text("utf-8").strip().split("\n\n")
        self.mazes = [MirrorMaze(content.split("\n")) for content in file_contents]

    def get_maze_checksum(self, tolerance: int = 0) -> int:
        return sum(maze.get_reflection_checksum(tolerance) for maze in self.mazes)


if __name__ == "__main__":
    assert Solution("example.txt").get_maze_checksum() == 405
    assert Solution("example.txt").get_maze_checksum(tolerance=1) == 400

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.get_maze_checksum()}")
    print(f"Solution 02: {puzzle_result.get_maze_checksum(tolerance=1)}")
