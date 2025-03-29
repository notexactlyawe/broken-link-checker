# Broken Link Checker (AI slop version)

**NOTE**: this project was built entirely to play around with AI tooling and may contain trace elements of slop. Tread with caution!

A simple utility that helps you find broken links on your website. It crawls through your site, identifies all links, and checks if they're working properly.

## What it does

- Crawls a website starting from a given URL
- Extracts all links from each page
- Checks each link for accessibility
- Groups and reports broken links by status code
- Handles both absolute and relative links

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/notexactlyawe/broken-link-checker
   cd broken-link-checker
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   
   # On Linux/macOS
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the checker:
   ```bash
   python broken_links.py https://example.com
   ```

   Just replace `https://example.com` with the website you want to check.

## Example Output

When the tool finds broken links, it will display a report like this:

```
===== BROKEN LINKS REPORT =====
Found 3 broken links:

== Status Code: 404 (2 links) ==
  • https://example.com/missing-page
    Found on: https://example.com/index

  • https://example.com/old-article
    Found on: https://example.com/blog

== Status Code: Connection Error (1 links) ==
  • https://non-existent-domain.com
    Found on: https://example.com/links
```
