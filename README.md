# adventus

_adventus_ is a set of helper functions for solving Advent of Code puzzles,
including functions for downloading input files and submitting answers.

## Example

```python
from adventus import Puzzle

def solve() -> None:
    """Solve the puzzle."""
    # initiate the puzzle
    puzzle = Puzzle({day}, {year})
    data = puzzle.input

    # solve path one
    puzzle.answer_one = None

    # solve part two
    puzzle.answer_two = None


if __name__ == "__main__":
    solve()
```

## AOC Server Friendly

_adventus_ follows the [AOC automation guidelines](https://www.reddit.com/r/adventofcode/wiki/faqs/automation) on r/adventofcode.

Specifically:

-   Outbound calls are throttled to 10 per minute (http module)
-   Once inputs are downloaded, they are cached locally (cache module)
-   If you suspect your cached input is corrupted, you can manually delete file
    in the cache directory (_.adventus_, by default)
-   The HTTP User-Agent header in the settings module is set to me since I maintain this tool.

## CLI Basic Usage

```sh
adventus {day} {year}
```

Automatically creates a source file from the template, runs the puzzle solver, 
and prompts the user to submit their answers

## Name Origin

_adventus_ is the Latin root for the word Advent,
which means arrival.
