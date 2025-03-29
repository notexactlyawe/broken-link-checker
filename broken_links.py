import requests
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

                # Determine if href is absolute or relative
                if href.startswith(("http://", "https://")):
                    all_links.append(href)
                else:
                    base_url = f"{url}{link['href']}"
                    all_links.append(base_url)

            return all_links
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return []
