#!/usr/bin/env python
"""\
Solution to https://adventofcode.com/2023/day/16

Usage: solution.py
"""

from dataclasses import dataclass, replace
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional, Tuple


class Direction(Enum):
    LEFT = auto()
    UP = auto()
    RIGHT = auto()
    DOWN = auto()


class GridElement(Enum):
    OFF = auto()
    ON = auto()
    MIRROR_RIGHT = auto()
    MIRROR_LEFT = auto()
    SPLITTER_HOR = auto()
    SPLITTER_VERT = auto()


Grid = List[List[GridElement]]


@dataclass
class Position:
    x: int
    y: int

    def step(self, direction: Direction) -> "Position":
        if direction == Direction.DOWN:
            return replace(self, y=self.y + 1)
        elif direction == Direction.LEFT:
            return replace(self, x=self.x - 1)
        elif direction == Direction.RIGHT:
            return replace(self, x=self.x + 1)
        elif direction == Direction.UP:
            return replace(self, y=self.y - 1)

    def __repr__(self) -> str:
        return f"(x={self.x}, y={self.y})"


class EGrid:
    def __init__(self, grid_repr: List[str]) -> None:
        self._length = len(grid_repr)
        self._width = len(grid_repr[0])

        self._energised: Grid = self._get_empty(width=self._width, length=self._length)
        self._map: Grid = self._map_to_grid(grid_repr)
        self.print_grid(self._map)

    def _get_empty(self, width: int, length: int) -> Grid:
        return [[GridElement.OFF for _ in range(width)] for _ in range(length)]

    def _grid_to_map(self, grid: Grid) -> str:
        def map_element_to_char(element: GridElement) -> str:
            if element == GridElement.OFF:
                return "."
            if element == GridElement.ON:
                return "#"
            if element == GridElement.MIRROR_RIGHT:
                return "/"
            if element == GridElement.MIRROR_LEFT:
                return "\\"
            if element == GridElement.SPLITTER_VERT:
                return "|"
            if element == GridElement.SPLITTER_HOR:
                return "-"
            raise ValueError(f"Cannot parse character: {element}")

        return "\n".join(["".join(map(map_element_to_char, row)) for row in grid])

    def _map_to_grid(self, grid_repr: List[str]) -> Grid:
        def map_char_to_element(char: str) -> GridElement:
            if char == ".":
                return GridElement.OFF
            if char == "#":
                return GridElement.ON
            if char == "/":
                return GridElement.MIRROR_RIGHT
            if char == "\\":
                return GridElement.MIRROR_LEFT
            if char == "|":
                return GridElement.SPLITTER_VERT
            if char == "-":
                return GridElement.SPLITTER_HOR
            raise ValueError(f"Cannot parse character: {char}")

        return [list(map(map_char_to_element, row)) for row in grid_repr]

    def _is_invalid_posistion(self, position: Position) -> bool:
        if position.x < 0 or position.x > self._width:
            return True
        if position.y < 0 or position.y > self._length:
            return True
        return False

    def energise_tiles(self, start: Position, direction: Direction) -> Grid:
        def energise_tile(pos: Position, dir: Direction) -> None:
            if self._is_invalid_posistion(pos):
                print(f"Invalid position: {pos}")
                return

            self._energised[pos.y][pos.x] = GridElement.ON
            print(f"Stepping {pos} to {dir}")
            el = self._map[pos.y][pos.x]
            new_pos = pos.step(dir)

            if dir == Direction.LEFT:
                if el == GridElement.MIRROR_LEFT:
                    energise_tile(new_pos, Direction.UP)
                elif el == GridElement.MIRROR_RIGHT:
                    energise_tile(new_pos, Direction.DOWN)
                elif el == GridElement.SPLITTER_VERT:
                    energise_tile(new_pos, Direction.UP)
                    energise_tile(new_pos, Direction.DOWN)
                else:
                    energise_tile(new_pos, Direction.LEFT)
            elif dir == Direction.RIGHT:
                if el == GridElement.MIRROR_LEFT:
                    energise_tile(new_pos, Direction.DOWN)
                elif el == GridElement.MIRROR_RIGHT:
                    energise_tile(new_pos, Direction.UP)
                elif el == GridElement.SPLITTER_VERT:
                    print("Going up...")
                    energise_tile(new_pos, Direction.UP)
                    print("Now going down...")
                    energise_tile(new_pos, Direction.DOWN)
                else:
                    energise_tile(new_pos, Direction.RIGHT)
            elif dir == Direction.UP:
                if el == GridElement.MIRROR_LEFT:
                    energise_tile(new_pos, Direction.LEFT)
                elif el == GridElement.MIRROR_RIGHT:
                    energise_tile(new_pos, Direction.RIGHT)
                elif el == GridElement.SPLITTER_HOR:
                    energise_tile(new_pos, Direction.LEFT)
                    energise_tile(new_pos, Direction.DOWN)
                else:
                    energise_tile(new_pos, Direction.UP)
            elif dir == Direction.DOWN:
                if el == GridElement.MIRROR_LEFT:
                    energise_tile(new_pos, Direction.RIGHT)
                elif el == GridElement.MIRROR_RIGHT:
                    energise_tile(new_pos, Direction.LEFT)
                elif el == GridElement.SPLITTER_HOR:
                    energise_tile(new_pos, Direction.LEFT)
                    energise_tile(new_pos, Direction.DOWN)
                else:
                    energise_tile(new_pos, Direction.DOWN)

        energise_tile(start, direction)
        self.print_grid(grid=self._energised)
        return self._energised

    def print_grid(self, grid: Optional[Grid] = None) -> None:
        if grid is None:
            grid = self._energised

        print(self._grid_to_map(grid))


class EnergiseGrid:
    def __init__(self, grid: str) -> None:
        self._grid = grid.split("\n")

    def get_energised_tiles(self) -> int:
        grid = EGrid(self._grid)
        grid.energise_tiles(start=Position(0, 0), direction=Direction.RIGHT)

        return 1


class Solution:
    def __init__(self, filename: str) -> None:
        file_contents = Path(filename).read_text("utf-8").strip()
        self.energised_grid = EnergiseGrid(grid=file_contents)

    def puzzle_01(self) -> int:
        return self.energised_grid.get_energised_tiles()

    def puzzle_02(self) -> int:
        return 0


if __name__ == "__main__":
    assert Solution("example.txt").puzzle_01() == 46
    # assert Solution("example.txt").puzzle_02() == 145

    puzzle_result = Solution("puzzle_input.txt")
    print(f"Solution 01: {puzzle_result.puzzle_01()}")
    # print(f"Solution 02: {puzzle_result.puzzle_02()}")
