"""Puzzle class."""

import logging
from functools import cached_property
from re import match

from bs4 import BeautifulSoup

from adventus.cache import read_answer, read_input, read_page
from adventus.settings import config

logger = logging.getLogger(__name__)


class Puzzle:
    """Puzzle class."""

    def __init__(self, day: int, year: int) -> None:
        """Initialize the class.

        Args:
            day (int): puzzle day
            year (int): puzzle year
        """
        self._day = day
        self._year = year

    @cached_property
    def day(self) -> int:
        """Puzzle day, 1 to 25.

        Returns:
            int: puzzle day
        """
        return self._day

    @cached_property
    def year(self) -> int:
        """Puzzle year, 2015 to current.

        Returns:
            int: puzzle year
        """
        return self._year

    @cached_property
    def title(self) -> str:
        """Puzzle title.

        Returns:
            str: title
        """
        return match(r"--- Day \d+: (.*) ---", self._page_soup.body.article.h2.text)[1]

    @cached_property
    def url(self) -> str:
        """Puzzle url.

        Returns:
            str: url
        """
        return f"{config.protocol}://{config.domain}/{self.year}/day/{self.day}"

    @cached_property
    def input(self) -> str:
        """Puzzle input file.

        Returns:
            str: input file data
        """
        return read_input(self.day, self.year).strip()

    @property
    def answers(self) -> tuple[str]:
        """Pair of answers, with None representing unsolved.

        Returns:
            tuple[str]: the answers for part one and part two
        """
        answers = [
            *(
                x.code.string
                for x in self._page_soup.find_all("p")
                if x.text.startswith("Your puzzle answer was")
            ),
            None,
            None,
        ]
        return tuple(answers[:2])

    @property
    def answer_one(self) -> str | None:
        """Answer one.

        Returns:
            str | None: the answer
        """
        return self._answers[0]

    @property
    def answer_two(self) -> str | None:
        """Answer two.

        Returns:
            str | None: the answer
        """
        return self._answers[1]

    @answer_one.setter
    def answer_one(self, value: int | str | None) -> bool:
        """Submit answer one.

        Args:
            value (int | str | None): the answer value

        Returns:
            bool: True if correct, else False.
        """
        return self._submit_answer(0, value)

    @answer_two.setter
    def answer_two(self, value: int | str | None) -> bool:
        """Submit answer two.

        Args:
            value (int | str | None): the answer value

        Returns:
            bool: True if correct, else False.
        """
        return self._submit_answer(1, value)

    def _submit_answer(self, part: int, value: int | str | None) -> bool:
        """Submit answers (internal function).

        Args:
            part (int): 0 for part one, 1 for part two
            value (int | str | None): the answer value

        Returns:
            bool: True if correct, else False.
        """
        name = ["Part One", "Part Two"]

        # coerce value into a string
        value = str(value)
        if self.answers[part]:
            # already solved
            if value != self.answers[part]:
                logger.warning(
                    "%s solved, but %s != %s", name[part], value, self.answers[part]
                )
                return False
            logger.info("%s solved, your answer is %d", {name[part]}, value)
            return True

        # check for silly answers
        if value == "None":
            logger.info("Skipping %s submission while answer is %s", name[part], value)
            return False

        # check if might be from example data
        if any(
            value in code.string
            for article in self._page_soup.find_all("article")
            for code in article.find_all("code")
        ):
            logger.warning(
                "Refusing to submit %s for %s - answer detected in puzzle example",
                value,
                name[part],
            )
            return False

        # submit answer
        prompt = input(
            f"Are you sure you want to submit {value} "
            f"as your answer to {name[part]}. (y/N)? "
        )
        if prompt.upper() == "Y" or prompt.upper() == "YES":
            logger.info("Submitting answer for %s: %s", name[part], value)
            html = read_answer(self.day, self.year, part + 1, value)
            soup = BeautifulSoup(html, "html.parser")
            message = soup.article.p.text
            logger.info(message)
            correct = "That's the right answer!" in message
            read_page(self.day, self.year, refresh=correct)
            return correct

        logger.info("User aborted answer submission")
        return False

    @property
    def _page_soup(self) -> BeautifulSoup:
        """Read the page and create soup.

        Returns:
            BeautifulSoup : the soup
        """
        page = read_page(self.day, self.year)
        return BeautifulSoup(page, "html.parser")
