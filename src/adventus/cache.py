"""Download and save files from Advent of Code website."""

import logging
from pathlib import Path
from re import search, sub
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from markdownify import ATX, BACKSLASH, MarkdownConverter

from adventus.http import get, post
from adventus.settings import config

logger = logging.getLogger(__name__)


def _read(url: str, local: Path, data: dict[str, str] | None = None) -> str:
    if not local.exists():
        logger.debug("Cache MISS: %s", url)
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text(post(url, data) if data else get(url))
    else:
        logger.debug("Cache HIT: %s", url)
    return local.read_text()


def read_input(day: int, year: int) -> str:
    """Read input file from cache.

    Args:
        day (int): puzzle day
        year (int): puzzle year

    Returns:
        str: the input file from the cache

    """
    url = f"{config.protocol}://{config.domain}/{year}/day/{day}/input"
    local = Path(f"{config.cache}/{year:04d}/{day:02d}/input.txt")
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
    page = Path(f"{config.cache}/{year:04d}/{day:02d}/page.html")
    puzzle = Path(f"{config.cache}/{year:04d}/{day:02d}/puzzle.md")
    if refresh:
        logger.debug("Purging cache for %s", url)
        page.unlink(missing_ok=True)
        puzzle.unlink(missing_ok=True)

    html = _read(url, page)
    if not puzzle.exists():
        puzzle.parent.mkdir(parents=True, exist_ok=True)
        puzzle.write_text(_html_to_markdown(day, year, html, url))

    return html


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


def _html_to_markdown(day: int, year: int, html: str, url:str) -> tuple[str, str]:
    """Read descriptions from cache.

    Args:
        day (int): puzzle day
        year (int): puzzle year
        html (str): the page html
        url (str): URL of the page

    Returns:
        str: the page
    """
    title = search(r"--- Day \d+: (.*) ---", html)[1]
    markdown = MarkdownConverter(
        heading_style=ATX,
        wrap=True,
        wrap_width=80,
        newline_style=BACKSLASH,
    )
    parts = "\n\n".join(
        markdown.convert_soup(article).strip()
        for article in BeautifulSoup(html, "html.parser").find_all(
            "article", attrs={"class": "day-desc"}
        )
    )
    parts = sub(
        r"## --- Day (\d+): (.*) ---\n",
        r"# Day \1: \2\n\n## --- Part One ---\n",
        parts,
    )

    return f"""\
---
title: {title}
date: {year:04d}-12-{day:02d}
author: Eric Wastl
url: {url}
---

{parts}
"""
