"""Adventus Commands."""

from pathlib import Path

from adventus.lib.settings import config
from adventus.lib.cache import cache
from adventus.lib.http import get

def fetch(day: int, year: int) -> str:
    cache(day, year)
    path = Path(f"{config.cache}/{year:04}/{day:02}/input.txt")
    if path.exists():
        return path.read_text()
    else:
        return get(f"{config.url}/{year}/day/{day}/input")


def submit(answer: str, day: int, year: int) -> bool:
    raise NotImplementedError