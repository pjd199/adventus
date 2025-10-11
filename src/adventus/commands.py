"""Adventus Commands."""

from importlib.resources import files
from pathlib import Path

from adventus.settings import config
from adventus.cache import cache
from adventus.http import get


def fetch(day: int, year: int) -> str:
    cache(day, year)
    path = Path(f"{config.cache}/{year:04}/{day:02}/input.txt")
    if path.exists():
        return path.read_text()
    else:
        return get(f"{config.url}/{year}/day/{day}/input")


def submit(answer: str, day: int, year: int) -> bool:
    print(answer)


def template(day: int, year: int) -> str:
    source = Path(config.source.format(day=day, year=year))
    if not source.exists():
        if Path(config.template).exists():
            code = Path(config.template).read_text()
        else:
            code = files("adventus").joinpath("template.txt").read_text()
        code = code.format(day=day, year=year)
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(code)
