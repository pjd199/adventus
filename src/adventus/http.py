"""HTTP interface."""

import logging

from requests import request

from adventus.settings import config

logger = logging.getLogger(__name__)


def get(url: str) -> str:
    """Send HTTP GET request for url.

    Args:
        url (str): url to get

    Returns:
        str: the result
    """
    logger.debug("GET %s HTTP/1.1", url)
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
