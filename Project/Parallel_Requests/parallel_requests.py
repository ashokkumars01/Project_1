from yarl import URL
import aiohttp
import asyncio
from typing import List, Dict, Optional
from Project.Logger import logging

async def fetch_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
    retries: int = 3
) -> Dict[str, Optional[dict]]:
    """
    Sends GET request with retry (max 3) and exponential backoff.
    """
    backoff = 1
    async with semaphore:
        
        for attempt in range(1, retries + 1):
            try:
                logging.info("Sends GET request with retry (max 3) and exponential backoff.")
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        json_data = await response.json()
                        print(f"[SUCCESS] {url}")
                        return {url: json_data}
                    else:
                        print(f"[ERROR {response.status}] {url}")
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message="Non-200 response",
                            headers=response.headers
                        )
            except Exception as e:
                logging.error(f"Error: {e}")
                print(f"[RETRY {attempt}] {url} - Error: {e}")
                if attempt < retries:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                else:
                    print(f"[FAILED] {url}")
                    return {url: None}


async def fetch_all_json(urls: List[str]) -> Dict[str, Optional[dict]]:
    """
    Fetch all valid URLs in parallel with max concurrency = 5.
    """
    results = {}
    try:
        logging.info("Fetch all valid URLs in parallel with max concurrency = 5.")
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_with_retry(session, url, semaphore) for url in urls]
            responses = await asyncio.gather(*tasks)
            for response in responses:
                results.update(response)
        return results
    except Exception as e:
        logging.error(f"Error: {e}")