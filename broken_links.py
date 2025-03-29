import argparse
import time
from dataclasses import dataclass
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


@dataclass
class BrokenLink:
    url: str
    status_code: int
    context_url: str


def extract_links(url, base_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return []

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for URL: {url}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    all_links = []
    for link in links:
        href = link["href"]

        # Check if it's a valid resource
        if not href or "#" in href:
            continue

        # Use urlparse to determine URL type and handle correctly
        parsed = urlparse(href)

        if parsed.scheme not in ("http", "https", ""):
            continue

        if parsed.netloc:
            all_links.append(href)
        else:
            # Handle relative URLs by joining with base URL
            absolute_url = urljoin(base_url, href)
            all_links.append(absolute_url)

    return all_links


def check_link_status(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Try HEAD request first (faster)
        response = requests.head(url, headers=headers, timeout=5)
        # Some servers don't handle HEAD requests properly, fallback to GET
        if response.status_code >= 400:
            response = requests.get(url, headers=headers, timeout=10)
        return response.status_code
    except requests.exceptions.RequestException:
        return 0  # 0 indicates connection error


def main(url: str):
    # get the base url
    base_url = urlparse(url).netloc
    visited_links = set()
    links_to_check = [url]
    broken_links = []

    try:
        while links_to_check:
            current_url = links_to_check.pop(0)

            if current_url in visited_links:
                continue

            print(f"Checking: {current_url}")
            visited_links.add(current_url)

            # Extract links from the current page
            page_links = extract_links(current_url, url)

            # Check each link and add new links to our queue
            for link in page_links:
                # Check if the link is broken
                status_code = check_link_status(link)
                if status_code >= 400 or status_code == 0:
                    # Save broken link information
                    broken_links.append(
                        BrokenLink(
                            url=link,
                            status_code=status_code,
                            context_url=current_url,
                        )
                    )

                # Only queue links from the same domain that we haven't visited
                parsed_link = urlparse(link)
                if (
                    parsed_link.netloc == base_url
                    and link not in visited_links
                    and link not in links_to_check
                ):
                    links_to_check.append(link)

        return broken_links

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Displaying results so far...")
        return broken_links


def display_results(broken_links):
    if not broken_links:
        print("\n✅ No broken links found!")
        return

    print("\n===== BROKEN LINKS REPORT =====")
    print(f"Found {len(broken_links)} broken links:\n")

    # Group by status code
    by_status = {}
    for link in broken_links:
        status = link.status_code
        if status not in by_status:
            by_status[status] = []
        by_status[status].append(link)

    # Display grouped results
    for status, links in sorted(by_status.items()):
        status_text = f"{status}" if status > 0 else "Connection Error"
        print(f"\n== Status Code: {status_text} ({len(links)} links) ==")

        for link in links:
            print(f"  • {link.url}")
            print(f"    Found on: {link.context_url}")
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for broken links on a website")
    parser.add_argument("url", help="The URL to check for broken links")
    args = parser.parse_args()

    start_time = time.time()
    print(f"Starting link check for: {args.url}")

    broken_links = main(args.url)

    elapsed_time = time.time() - start_time
    print(f"\nCompleted in {elapsed_time:.2f} seconds")

    display_results(broken_links)
