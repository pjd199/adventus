"""Download and save files from Advent of Code website."""

import logging
from pathlib import Path
from urllib.parse import quote_plus

from adventus.http import get, post
from adventus.settings import config

logger = logging.getLogger(__name__)


def _read(url: str, local: str, data: dict[str, str] | None = None) -> str:
    file = Path(local)
    if not file.exists():
        logger.debug("Cache MISS: %s", url)
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(post(url, data) if data else get(url))
    else:
        logger.debug("Cache HIT: %s", url)
    return file.read_text()


def _purge(url: str, local: str) -> str:
    logger.debug("Purging cache for %s", url)
    file = Path(local)
    if file.exists():
        file.unlink()


def read_input(day: int, year: int) -> str:
    """Read input file from cache.

    Args:
        day (int): puzzle day
        year (int): puzzle year

    Returns:
        str: the input file from the cache

    """
    url = f"{config.protocol}://{config.domain}/{year}/day/{day}/input"
    local = f"{config.cache}/{year:04d}/{day:02d}/input.txt"
    return _read(url, local)


def read_page(day: int, year: int, refresh: bool = False) -> str:
    """Read page from cache.

    Args:
        day (int): puzzle day
        year (int): puzzle year
        refresh (bool, optional): if True, refresh cache. Defaults to False.

    Returns:
        str: the page
    """
    url = f"{config.protocol}://{config.domain}/{year}/day/{day}"
    local = f"{config.cache}/{year:04d}/{day:02d}/page.html"
    if refresh:
        _purge(url, local)
    return _read(url, local)


def read_answer(day: int, year: int, level: int, answer: str) -> str:
    """Read answer from cache.

    Args:
        day (int): puzzle day
        year (int): puzzle year
        level (int): puzzle level 1 = part one, 2 = part two
        answer (str): answer to submit

    Returns:
        str: the submission response
    """
    url = f"{config.protocol}://{config.domain}/{year}/day/{day}/answer"
    local = (
        f"{config.cache}/{year:04d}/{day:02d}/answer/{level}/{quote_plus(answer)}.html"
    )
    return _read(url, local, {"level": level, "answer": answer})
