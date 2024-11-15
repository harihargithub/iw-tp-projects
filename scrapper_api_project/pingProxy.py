# pingProxy.py

import requests

proxy = "http://103.216.82.153:6666"  # Example proxy
proxies = {"http": proxy, "https": proxy}

try:
    response = requests.get("http://quotes.toscrape.com/", proxies=proxies, timeout=5)
    if response.status_code == 200:
        print("Proxy works!")
    else:
        print("Proxy may be blocked or unresponsive.")
except Exception as e:
    print(f"Proxy failed: {e}")
