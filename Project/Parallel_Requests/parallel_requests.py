from yarl import URL # Used for parsing and validating URL components
import aiohttp  # For asynchronous HTTP requests
import asyncio  # For managing asynchronous event loop and concurrency
from typing import List, Dict, Optional
from Project.Logger import logging  # Custom logging utility for project
from Project.Constants.constants import *

# -----------------------------------------------
# Function: fetch_with_retry
# Purpose: Sends GET request to a URL with up to 3 retries and exponential backoff
# -----------------------------------------------
async def fetch_with_retry(
    session: aiohttp.ClientSession,  # Reusable session for efficient requests
    url: str,                        # URL to fetch
    semaphore: asyncio.Semaphore,    # Controls max concurrent requests
    retries: RETRY                   # Number of retry attempts (default 3)
) -> Dict[str, Optional[dict]]:
    """
    Sends GET request with retry (max 3) and exponential backoff.
    Returns a dictionary with URL as key and JSON response or None as value.
    """
    backoff = BACKOFF  # Initial delay between retries
    
    # Acquire the semaphore before making request (limits concurrency)
    async with semaphore:
        for attempt in range(1, retries + 1):
            try:
                logging.info("Sends GET request with retry (max 3) and exponential backoff.")
                
                # Make GET request with 10-second timeout
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        # Successfully received JSON data
                        json_data = await response.json()
                        print(f"[SUCCESS] {url}")
                        return {url: json_data}
                    else:
                        # Received non-200 HTTP response
                        print(f"[ERROR {response.status}] {url}")
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message="Non-200 response",
                            headers=response.headers
                        )
            except Exception as e:
                # Log error and retry if attempts remain
                logging.error(f"Error: {e}")
                print(f"[RETRY {attempt}] {url} - Error: {e}")
                if attempt < retries:
                    await asyncio.sleep(backoff)  # Wait before retrying
                    backoff *= 2  # Exponential backoff
                else:
                    # All attempts failed
                    print(f"[FAILED] {url}")
                    return {url: None}


# -----------------------------------------------
# Function: fetch_all_json
# Purpose: Fetch JSON data from multiple URLs concurrently (max 5 at a time)
# -----------------------------------------------
async def fetch_all_json(urls: List[str]) -> Dict[str, Optional[dict]]:
    """
    Fetch all valid URLs in parallel with max concurrency = 5.
    Returns a dictionary of URLs mapped to their JSON responses or None.
    """
    results = {}  # Initialize dictionary to hold results
    
    try:
        logging.info("Fetch all valid URLs in parallel with max concurrency = 5.")
        
        # Semaphore to allow only 5 concurrent HTTP requests
        semaphore = asyncio.Semaphore(SEMAPHORE_COUNT)
        
        # Create and use a single aiohttp session for all requests
        async with aiohttp.ClientSession() as session:
            # Prepare list of coroutine tasks to fetch each URL
            tasks = [fetch_with_retry(session, url, semaphore) for url in urls]
            
            # Execute all tasks concurrently and wait for results
            responses = await asyncio.gather(*tasks)
            
            # Combine all individual dictionaries into one final result
            for response in responses:
                results.update(response)
        return results
    except Exception as e:
        # Catch and log any unexpected errors
        logging.error(f"Error: {e}")