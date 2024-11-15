# quotesProxyTest.py

import requests

url = "http://quotes.toscrape.com/"
proxies = {"http": "http://103.216.82.153:6666"}  # Use a working proxy here
response = requests.get(url, proxies=proxies)
print(response.text)
