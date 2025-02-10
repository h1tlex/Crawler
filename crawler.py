import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def crawl(url, max_pages=5, visited=None):
    """
    A simple web crawler that recursively fetches and processes links from a webpage.

    Parameters:
    - url (str): The starting URL to crawl.
    - max_pages (int): Maximum number of pages to visit.
    - visited (set): A set to keep track of visited URLs and prevent repetition.
    """
    if visited is None:
        visited = set()  # Initialize visited URLs set

    if url in visited or len(visited) >= max_pages:
        return  # Stop if max pages are visited or URL is already processed

    print(f"Crawling: {url}")  # Display the URL being crawled
    visited.add(url)  # Mark the URL as visited

    if content == 'Y':
        extract_content(url) # Extract content from current URL
    if images == 'Y':
        extract_images(url) # Extract images from current URL

    try:
        # Fetch the webpage content
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all anchor tags with an href attribute (links)
        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])  # Convert relative URLs to absolute
            if next_url.startswith('http'):  # Ensure the link is a valid webpage
                crawl(next_url, max_pages, visited)  # Recursively crawl the new URL

    except requests.exceptions.RequestException as e:
        print(f"Failed to crawl {url}: {e}")  # Handle exceptions like timeout or bad requests

def extract_content(url):
    """Fetches and extracts the title and main text from a webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract page title
        title = soup.title.string if soup.title else "No title"

        # Extract visible text content (excluding scripts and styles)
        text = ' '.join(p.text.strip() for p in soup.find_all('p'))

        print(f"Title: {title}\nText: {text[:300]}...")  # Show first 300 chars
    except requests.exceptions.RequestException as e:
        print(f"Failed to extract content from {url}: {e}")


def extract_images(url):
    """Fetches and extracts image URLs from a webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract image URLs
        images = [urljoin(url, img['src']) for img in soup.find_all('img', src=True)]

        print(f"Found {len(images)} images:")
        for img in images[:5]:  # Show only first 5 images
            print(img)

    except requests.exceptions.RequestException as e:
        print(f"Failed to extract images from {url}: {e}")



if __name__ == "__main__":

    argc = len(sys.argv)

    if argc != 3:
        print(f"Usage: {sys.argv[0]} <url> <max_pages>\n", file=sys.stderr)
        sys.exit(1)

    content = input("Would you like to extract content from visited URLs? [Y/n]\n")
    images = input("Would you like to extract images from visited URLs? [Y/n]\n")

    # Start crawling from an initial webpage
    start_url = sys.argv[1]
    max_pages = int(sys.argv[2])
    crawl(start_url, max_pages)

