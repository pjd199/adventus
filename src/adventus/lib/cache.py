"""Download and save files from Advent of Code website."""

from datetime import datetime, UTC
from pathlib import Path
from adventus.lib.settings import config
from adventus.lib.http import get

from bs4 import BeautifulSoup
from markdownify import ATX, markdownify  # type: ignore


def save(data: str, path: Path, overwrite=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite or (not path.exists() or path.read_text() != data):
        path.write_text(data)


def cache(day: int, year: int) -> None:
    url = f"{config.url}/{year}/day/{day}"
    cache_path = Path(f"{config.cache}/{year:04}/{day:02}")
    input_path = cache_path / "input.txt"
    puzzle_path = cache_path / "puzzle.md"
    answer_one_path = cache_path / "answer_one.txt"
    answer_two_path = cache_path / "answer_two.txt"

    # download and save the input, if required
    if config.cache_input and not input_path.exists():
        save(get(f"{url}/input"), input_path)

    # download puzzle page if required
    if (config.cache_puzzle and not puzzle_path.exists()) or (
        config.cache_answers
        and (not answer_one_path.exists() or not answer_two_path.exists())
    ):
        page = get(url)
        soup = BeautifulSoup(page, "html.parser")
        overwrite = False

        if config.cache_answers:
            answers = [
                x.code.string
                for x in soup.find_all("p")
                if x.text.startswith("Your puzzle answer was")
            ]
            for answer, path in zip(answers, [answer_one_path, answer_two_path]):
                if not path.exists():
                    save(answer, path)
                    overwrite = True

        if config.cache_puzzle:
            save(
                f"# {soup.head.title.contents[0]}\n\n"
                + f"{url}\n{datetime.now(UTC).isoformat(timespec="seconds")}\n\n"
                + "\n".join(
                    markdownify(str(x), heading_style=ATX, wrap=80)
                    for x in soup.find_all("article")
                ),
                puzzle_path,
                overwrite,
            )
