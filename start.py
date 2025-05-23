from Project.Validation.url_validation import is_url_reachable, validate_urls, is_valid_format  # URL validation functions
from Project.Logger import logging  # Custom logging configuration
import asyncio  # Async I/O framework
import aiohttp  # HTTP client for async requests
from yarl import URL  # URL parser and validator
import time  # Used for tracking execution time
from Project.Parallel_Requests.parallel_requests import fetch_all_json, fetch_with_retry  # Async fetch functions


# -------------------------------------------------------
# MAIN FUNCTION: Orchestrates the full pipeline
# -------------------------------------------------------
def main():
    """
    Main function to coordinate URL validation, data fetching with retry and parallelism, and logging.
    """
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
        "https://jsonplaceholder.typicode.com/posts/5",
        "https://jsonplaceholder.typicode.com/posts/6",
        "http://example.com",  # Valid format but likely not a JSON response
        "ftp://invalid.com",   # Invalid scheme (not http or https)
        "https://invalid.url.fake"  # Invalid or unreachable domain
    ]
    

    # ---------------------------------------------------
    # Record the start time to calculate total execution time
    # ---------------------------------------------------
    start_time = time.time()

    # ---------------------------------------------------
    # Step 1: Validate the URL format and reachability
    # Uses is_valid_format() and is_url_reachable()
    # ---------------------------------------------------
    print("\n[STEP 1] Validating URLs...")
    valid_urls = asyncio.run(validate_urls(urls))  # Filter valid and reachable URLs
    print(f"\n[INFO] Valid & Reachable URLs: {len(valid_urls)}")

    # ---------------------------------------------------
    # Step 2: Fetch JSON responses from all valid URLs
    # Uses parallelism with concurrency control and retries
    # ---------------------------------------------------
    print("\n[STEP 2] Fetching JSON responses...")
    json_results = asyncio.run(fetch_all_json(valid_urls))  # Fetch all responses in parallel

    # ---------------------------------------------------
    # Step 3: Print a summary of fetch results (success/failure)
    # ---------------------------------------------------
    print("\n[RESULTS]")
    for url, result in json_results.items():
        status = "Success" if result else "Failed"
        print(f"{url}: {status}")
        
    # ---------------------------------------------------
    # Step 4: Print the actual JSON data from each successful request
    # ---------------------------------------------------
    print("\n[PARSED JSON RESULTS]")
    for url, json_data in json_results.items():
        if json_data is not None:
            print(f"{url}:\n{json_data}\n")
        else:
            print(f"{url}: Failed or not JSON\n")

    # ---------------------------------------------------
    # Step 5: Print total execution time of the pipeline
    # ---------------------------------------------------
    total_time = time.time() - start_time
    print(f"\n[TIME TAKEN] {total_time:.2f} seconds")
    

if __name__ == "__main__":
    main()