from yarl import URL
import aiohttp
import asyncio
from typing import List, Dict, Optional
from Project.Logger import logging


def is_valid_format(url: str) -> bool:
    """
    Validates if the URL is properly formatted (http or https).
    """
    try:
        logging.info("Started parsing the URL")
        parsed = URL(url)
        if parsed.scheme in {"http", "https"} and parsed.host is not None:
            logging.info("Given URL is in Valid format")
            return True
    except Exception as e:
        logging.error(f"Error while checking format: {url} - {e}")
        return False


async def is_url_reachable(session: aiohttp.ClientSession, url: str) -> bool:
    """
    Sends a HEAD request to check if URL is reachable.
    """
    try:
        logging.info("Checking whether the URL is reachable or not")
        async with session.head(url, timeout=5) as response:
            return response.status < 400
    except Exception as e:
        logging.error(f"Error while checking reachability: {url} - {e}")
        return False


async def validate_urls(urls: List[str]) -> List[str]:
    """
    Validates the format and reachability of URLs.
    """
    valid_urls = []
    try:
        logging.info("Started validating format of the list of URLs")
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                if is_valid_format(url):
                    tasks.append((url, is_url_reachable(session, url)))
                else:
                    print(f"[INVALID FORMAT] {url}")
            logging.info("Started validating format of the list of URLs Completed")

            logging.info("Started checking all the URLs are reachable or not")
            results = await asyncio.gather(*(task for _, task in tasks))
            for (url, _), reachable in zip(tasks, results):
                if reachable:
                    valid_urls.append(url)
                else:
                    print(f"[UNREACHABLE] {url}")
            logging.info("Started checking all the URLs are reachable Completed")
        return valid_urls
    except Exception as e:
        logging.error(f"Error while checking reachability and format: {url} - {e}")
