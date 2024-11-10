# quotes2scrape.py

import requests
from bs4 import BeautifulSoup


def scrape_data():
    url = "http://quotes.toscrape.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Example: Extract quotes and authors
        quotes = [
            {
                "text": quote.find("span", class_="text").get_text(),
                "author": quote.find("small", class_="author").get_text(),
            }
            for quote in soup.find_all("div", class_="quote")
        ]
        return {"quotes": quotes}
    else:
        return {"error": "Failed to retrieve data"}
