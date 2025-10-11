from tomllib import loads
from functools import cache
from os import getenv
from pathlib import Path
from dataclasses import dataclass


@cache
def configuration():
    path = Path("pyproject.toml")
    if path.exists():
        file = loads(path.read_text())
        if "tools" in file and "adventus" in file["tools"]:
            return file["tools"]["adventus"]
    return {}


@dataclass(frozen=True)
class Config:
    url = "https://adventofcode.com"
    cache = configuration().get("cache", ".adventus")
    session = getenv("AOC_SESSION", "")
    user_agent = "https://github.com/pjd199/adventus"
    cache_input = configuration().get("cache-input", True)
    cache_puzzle = configuration().get("cache-puzzle", False)
    cache_answers = configuration().get("cache-answers", True)
    template = configuration().get("template", ".adventus/template.py")
    source = configuration().get("source", "src/adventofcode/year{year:04d}/day{day:02d}.py")

config = Config()