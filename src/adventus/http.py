"""HTTP interface."""

from requests import request

from adventus.settings import config


def get(url: str):
    response = request(
        "GET",
        url,
        headers={
            "User-Agent": config.user_agent,
            "cookie": f"session={config.session}",
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.text
