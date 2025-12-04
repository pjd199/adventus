"""Advent of Code 2025.

Day 3: Lobby

https://adventofcode.com/2025/day/3
"""

from adventus import Puzzle


def solve() -> None:
    """Solve the puzzle."""
    # initiate the puzzle
    puzzle = Puzzle(3, 2025)
    data = puzzle.input

    # solve part one
    puzzle.answer_one = 123456e767

    # solve part two
    puzzle.answer_two = None


if __name__ == "__main__":
    solve()
