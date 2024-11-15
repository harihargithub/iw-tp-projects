# quotesWoProxyTest.py

import requests

response = requests.get("http://quotes.toscrape.com/")
print(response.text)
