import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def extract_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
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
                
                if parsed.netloc:
                    all_links.append(href)
                else:
                    # Handle relative URLs by joining with base URL
                    base_url = url + parsed.path
                    if not parsed.path.startswith('/'):
                        base_url = url + parsed.path
                    all_links.append(base_url)

            return all_links
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return []
