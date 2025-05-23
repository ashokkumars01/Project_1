from yarl import URL
import aiohttp
import asyncio
from typing import List, Dict, Optional
from Project.Logger import logging


# ----------------------------------------------
# Function: is_valid_format
# Purpose: Checks if a URL has a valid format (scheme and host present)
# ----------------------------------------------
def is_valid_format(url: str) -> bool:
    """
    Validates if the URL is properly formatted (starts with http or https and has a host).
    """
    try:
        logging.info("Started parsing the URL")

        parsed = URL(url)  # Parse the input URL
        if parsed.scheme in {"http", "https"} and parsed.host is not None:
            logging.info("Given URL is in Valid format")
            return True  # Valid format
    except Exception as e:
        logging.error(f"Error while checking format: {url} - {e}")
        return False  # Return False if parsing fails or scheme/host is invalid


# ----------------------------------------------
# Function: is_url_reachable
# Purpose: Uses a HEAD request to check if a URL is reachable
# ----------------------------------------------
async def is_url_reachable(session: aiohttp.ClientSession, url: str) -> bool:
    """
    Sends a HEAD request to check if the URL is reachable (status code < 400).
    """
    try:
        logging.info("Checking whether the URL is reachable or not")
        async with session.head(url, timeout=5) as response:
            return response.status < 400  # True if reachable (status code < 400)
    except Exception as e:
        logging.error(f"Error while checking reachability: {url} - {e}")
        return False  # Unreachable or exception occurred


# ----------------------------------------------
# Function: validate_urls
# Purpose: Validates list of URLs for both format and reachability
# ----------------------------------------------
async def validate_urls(urls: List[str]) -> List[str]:
    """
    Validates the format and reachability of a list of URLs.
    Returns a list of URLs that are valid and reachable.
    """
    valid_urls = []  # To store successfully validated URLs
    
    try:
        logging.info("Started validating format of the list of URLs")
        async with aiohttp.ClientSession() as session:  # Shared session for efficiency
            tasks = []  # Stores (url, reachability_task) pairs
            
            # Step 1: Check format of each URL
            for url in urls:
                if is_valid_format(url):
                    # Add tuple of (url, coroutine to check reachability)
                    tasks.append((url, is_url_reachable(session, url)))
                else:
                    print(f"[INVALID FORMAT] {url}")
            logging.info("Started validating format of the list of URLs --> Completed")

            # Step 2: Run all reachability checks concurrently
            logging.info("Started checking all the URLs are reachable or not")
            results = await asyncio.gather(*(task for _, task in tasks))  # Run all coroutines
            
            # Step 3: Combine results with corresponding URLs
            for (url, _), reachable in zip(tasks, results):
                if reachable:
                    valid_urls.append(url)
                else:
                    print(f"[UNREACHABLE] {url}")
            logging.info("Started checking all the URLs are reachable --> Completed")
        return valid_urls
    
    except Exception as e:
        # Handle and log any unexpected error during format/reachability check
        logging.error(f"Error while checking reachability and format: {url} - {e}")
