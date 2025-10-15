"""HTTP interface."""

import logging
import tempfile
from pathlib import Path

from pyrate_limiter import Duration, Limiter, Rate, SQLiteBucket
from requests import request

from adventus.settings import config

logger = logging.getLogger(__name__)

# configure the rate limiter
rate = Rate(config.requests_per_minute, Duration.MINUTE)
bucket = SQLiteBucket.init_from_file(
    [rate],
    db_path=str(Path(tempfile.gettempdir()) / "adventus-limiter.sqlite"),
    use_file_lock=True,
)
limiter = Limiter(bucket, raise_when_fail=False, max_delay=60 * 1000)


def get(url: str) -> str:
    """Send HTTP GET request for url.

    Args:
        url (str): url to get

    Returns:
        str: the result
    """
    logger.debug("GET %s HTTP/1.1", url)
    limiter.try_acquire(url)
    response = request(
        "GET",
        url,
        headers={
            "User-Agent": config.user_agent,
            "cookie": f"session={config.session}",
        },
        timeout=60,
    )
    logger.debug("HTTP/1.1 %d %s", response.status_code, response.reason)
    response.raise_for_status()
    return response.text


def post(url: str, data: dict[str, str]) -> str:
    """Send HTTP POST for url, with data.

    Args:
        url (str): the url
        data (dict[str, str]): the data, a dict of string key/value pairs

    Returns:
        str: the response
    """
    logger.debug("POST %s HTTP/1.1 %s", url, str(data))
    limiter.try_acquire(url)
    response = request(
        "POST",
        url,
        headers={
            "User-Agent": config.user_agent,
            "cookie": f"session={config.session}",
        },
        timeout=60,
        data=data,
    )
    logger.debug("HTTP/1.1 %d %s", response.status_code, response.reason)
    response.raise_for_status()
    return response.text
