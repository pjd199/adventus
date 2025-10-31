"""CLI for downloading Advent of Code puzzle input and submitting answers."""

import logging
from argparse import ArgumentParser
from datetime import UTC, datetime
from importlib.resources import files
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from adventus.puzzle import Puzzle
from adventus.settings import config

logger = logging.getLogger(__name__)


def template(day: int, year: int) -> None:
    """Create a source file from the template.

    Args:
        day (int): puzzle day
        year (int): puzzle year
    """
    puzzle = Puzzle(day, year)
    source = Path(config.source.format(day=day, year=year))
    if not source.exists():
        if Path(config.template).exists():
            code = Path(config.template).read_text()
        else:
            code = files("adventus").joinpath("template.txt").read_text()
        code = code.format(
            day=puzzle.day, year=puzzle.year, title=puzzle.title, url=puzzle.url
        )
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(code)


def execute(day: int, year: int) -> None:
    """Execute a puzzle solver.

    Args:
        day (int): puzzle day
        year (int): puzzle year
    """
    file = Path(config.source.format(day=day, year=year))
    logger.info("Loading %s", file)
    spec = spec_from_file_location(f"temp_{year}_{day}", file)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    function = getattr(module, config.entry)
    function()


def cli() -> int:
    """Command Line Interface functionality.

    Returns:
        int: the return code, usually 0.
    """
    now = datetime.now(UTC)
    days = list(range(1, 26))
    years = list(range(2015, now.year + 1 if now.month == 12 else now.year))

    parser = ArgumentParser(
        description="Download input file from the Advent of Code website."
    )
    parser.add_argument(
        "year",
        type=int,
        nargs="?",
        choices=years,
        default=years[-1],
        help="the year of the puzzle input to download",
    )
    parser.add_argument(
        "day",
        type=int,
        nargs="?",
        choices=days,
        default=days[-1],
        help="the day of the puzzle input to download",
    )
    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument("-q", "--quiet", "--silent", action="store_true", help="quiet mode")
    logging_group.add_argument(
        "-v", "--verbose", action="store_true", help="verbose mode"
    )
    args = parser.parse_args()

    # configure logging
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=(
            logging.WARNING
            if args.quiet
            else logging.DEBUG
            if args.verbose
            else logging.INFO
        ),
    )

    # check for session
    if config.session is None:
        logger.critical("AOC_SESSION environment variable not set.")
        return 1

    template(args.day, args.year)
    execute(args.day, args.year)

    return 0


if __name__ == "__main__":
    cli()
