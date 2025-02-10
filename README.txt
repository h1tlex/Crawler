A simple web crawler that recursively fetches and processes links from a webpage
with the option to extract content and images.

    Parameters:
    - url (str): The starting URL to crawl.
    - max_pages (int): Maximum number of pages to visit.
    - visited (set): A set to keep track of visited URLs and prevent repetition.

Usage :
	Python3 crawler.py <url> <max_pages>
Options :
	Use URL content extractor : 
		Fetches and extracts the title and main text from a webpage.
	Use URL image extractor :
		Fetches and extracts image URLs from a webpage.