#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/13

Usage: solution.py
"""

from enum import Enum, auto
from pathlib import Path
from typing import List, Optional

import numpy as np


class Direction(Enum):
    """Describes matrix reflection orientation"""
    VERTICAL = auto()
    HORIZONTAL = auto()
    UNKNOWN = auto()


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
            return -1
        elif char == "#":
            return 1
        else:
            raise RuntimeError(f"Unexpected character: {char}")

    def get_reflection_checksum(self) -> int:
        """Get reflection checksum for the matrix"""

        # Start vertical
        orientation = Direction.UNKNOWN
        reflect_index = self._symmetric_submatrix_column(self.maze)
        if reflect_index:
            orientation = Direction.VERTICAL
        else:
            orientation = Direction.HORIZONTAL
            self.maze = np.rot90(self.maze)
            reflect_index = self._symmetric_submatrix_column(self.maze)
            if not reflect_index:
                raise RuntimeError(f"No reflection found for matrix:\n{self.maze}")

        if orientation is Direction.VERTICAL:
            return reflect_index
        elif orientation is Direction.HORIZONTAL:
            return 100 * reflect_index
        else:
            raise RuntimeError("Failing to detect symmetricitiyity. :()")

    def _symmetric_submatrix_column(self, matrix: np.ndarray) -> Optional[int]:
        columns = matrix.shape[1]
        max_window_size = columns if columns % 2 == 0 else columns - 1
        min_window_size = 4

        for window_size in range(max_window_size, min_window_size - 1, -2):
            for start_index in range(0, columns - window_size + 1):
                submatrix = matrix[:, start_index:start_index+window_size]
                if self._is_matrix_symmetric(submatrix):
                    return start_index + window_size // 2
        return None

    def _is_matrix_symmetric(self, matrix: np.ndarray) -> bool:
        columns = matrix.shape[1]
        if columns % 2 != 0:
            raise RuntimeError("Cannot determine if matrix of uneven columns are vertically semitrical.")
        left = matrix[:, columns // 2:]
        right = np.fliplr(matrix[:, :columns // 2])
        return np.array_equal(left, right)


class Solution:
    """Loads in the Mirror Maze and processes it."""

    def __init__(self, filename: str) -> None:
        file_contents: List[str] = Path(filename).read_text('utf-8').strip().split('\n\n')
        self.mazes: List[MirrorMaze] = []
        for content in file_contents:
            self.mazes.append(MirrorMaze(content.split()))

    def get_maze_checksum(self) -> int:
        """Solution for puzzle 01"""
        checksum = 0
        for maze in self.mazes:
            checksum += maze.get_reflection_checksum()
        return checksum


if __name__ == '__main__':
    assert Solution("example.txt").get_maze_checksum() == 405
