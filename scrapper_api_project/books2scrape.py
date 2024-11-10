# books2scrape.py

import requests
from bs4 import BeautifulSoup


def scrape_data():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Example: Extract book titles
        books = [book.get_text() for book in soup.find_all("h3")]
        return {"books": books}
    else:
        return {"error": "Failed to retrieve data"}
