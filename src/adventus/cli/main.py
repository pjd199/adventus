"""CLI for downloading Advent of Code puzzle input and submitting answers."""

from argparse import ArgumentParser
from datetime import datetime, UTC

from adventus.lib.settings import config
from adventus.lib.commands import fetch, submit


def main() -> int:
    """Main function, called from the command line.

    Returns:
        int: the return code, usually 0.
    """
    if not config.session:
        print("AOC_SESSION environment variable not set.")
        return 1
    now = datetime.now(UTC)
    days = list(range(1, 26))
    years = list(range(2015, now.year + 1 if now.month == 12 else now.year))

    parser = ArgumentParser(
        description="Download input file from the Advent of Code website."
    )
    parser.add_argument(
        "day",
        type=int,
        nargs="?",
        choices=days,
        default=days[-1],
        help="the day of the puzzle input to download",
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
        "--fetch",
        action="store_true",
        default=False,
        help="fetch the puzzle input",
    )

    parser.add_argument(
        "--submit",
        action="store_true",
        default=False,
        help="submit the puzzle answers",
    )
    args = parser.parse_args()

    # fetch the input file
    data = fetch(args.day, args.year)
    if args.fetch:
        print(data)

    # submit the answers
    if args.submit:
        submit(-1, args.day, args.year)

    return 0


if __name__ == "__main__":
    main()
