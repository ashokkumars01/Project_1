from Project.Validation.url_validation import is_url_reachable, validate_urls, is_valid_format
from Project.Logger import logging
import asyncio
import aiohttp
from yarl import URL
import time
from Project.Parallel_Requests.parallel_requests import fetch_all_json, fetch_with_retry

def main():
    """
    Main function to coordinate validation, fetching, and logging.
    """
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
        "https://jsonplaceholder.typicode.com/posts/5",
        "https://jsonplaceholder.typicode.com/posts/6",
        "http://example.com",  # Not JSON
        "ftp://invalid.com",   # Invalid scheme
        "https://invalid.url.fake"  # Unreachable
    ]
    # urls = [
    # "https://www.google.com",
    # "https://www.github.com",
    # "https://www.python.org",
    # "https://www.wikipedia.org",
    # "http://example.com",  # Not JSON
    # "ftp://invalid.com",   # Invalid scheme
    # "https://invalid.url.fake"  # Unreachable
# ]


    start_time = time.time()

    # Step 1: Validate URLs
    print("\n[STEP 1] Validating URLs...")
    valid_urls = asyncio.run(validate_urls(urls))
    print(f"\n[INFO] Valid & Reachable URLs: {len(valid_urls)}")

    # Step 2–6: Fetch data with retry and parallelism
    print("\n[STEP 2] Fetching JSON responses...")
    json_results = asyncio.run(fetch_all_json(valid_urls))

    # Step 7: Print Results Summary
    print("\n[RESULTS]")
    for url, result in json_results.items():
        status = "Success" if result else "Failed"
        print(f"{url}: {status}")
        
    # Step 8: Print Parsed JSON Results
    print("\n[PARSED JSON RESULTS]")
    for url, json_data in json_results.items():
        if json_data is not None:
            print(f"{url}:\n{json_data}\n")
        else:
            print(f"{url}: Failed or not JSON\n")

    # Step 9: Log time
    total_time = time.time() - start_time
    print(f"\n[TIME TAKEN] {total_time:.2f} seconds")
    
if __name__ == "__main__":
    main()