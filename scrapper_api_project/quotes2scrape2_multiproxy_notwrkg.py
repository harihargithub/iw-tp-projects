# quotes2scrape2_workingWell2.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
import random
import os
import time

# Path to your locally downloaded ChromeDriver (assuming it's extracted)
CHROME_DRIVER_PATH = "C:\\Program Files\\chrome\\chromedriver-win64\\chromedriver.exe"  # Adjust if different

# Verify that the ChromeDriver path is correct
if not os.path.exists(CHROME_DRIVER_PATH):
    raise FileNotFoundError(f"ChromeDriver not found at {CHROME_DRIVER_PATH}")

# List of user agents (example)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.3 Safari/602.3.12",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
    # Add more user agents here
]

# List of provided proxies
PROXIES = [
    "89.116.78.223:5834",
    "173.211.0.187:6680",
    "188.132.222.56:8080",
    "142.44.210.174:80",
    "206.189.184.55:80",
    "107.172.156.96:5744",
    "156.228.104.239:3128",
    "156.228.76.40:3128",
    "45.146.30.106:6610",
    "156.228.124.154:3128",
    "201.151.252.120:80",
    "104.207.47.50:3128",
    "47.89.159.212:31281",
    "156.228.89.179:3128",
    "178.128.49.205:80",
    "207.244.217.125:6672",
    "138.128.153.98:5132",
    "104.207.34.90:3128",
    "104.250.207.236:6634",
    "104.207.56.247:3128",
    "103.49.202.252:80",
    "191.101.41.19:6091",
    "156.228.108.14:3128",
    "106.42.30.243:82",
    "156.228.115.254:3128",
    "192.177.86.117:5118",
    "136.0.117.215:6953",
    "212.42.203.12:6060",
    "156.228.119.193:3128",
    "156.228.76.152:3128",
    "217.168.76.83:3128",
    "156.228.76.177:3128",
    "156.228.124.5:3128",
    "114.236.93.208:42611",
    "104.207.47.191:3128",
    "102.209.18.68:8080",
    "35.161.172.205:3128",
    "47.90.205.231:33333",
    "104.143.252.95:5709",
    "107.181.152.160:5197",
    "159.65.245.255:80",
    "198.199.81.151:80",
    "173.208.211.82:17034",
]


def get_random_proxy():
    return random.choice(PROXIES)


def get_random_user_agent():
    return random.choice(USER_AGENTS)


def random_delay(min_delay=1, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))


def scrape_data():
    url = "http://quotes.toscrape.com/"

    # Set up proxy
    proxy = get_random_proxy()
    proxy_options = Proxy()
    proxy_options.proxy_type = ProxyType.MANUAL
    proxy_options.socks_proxy = f"socks4://{proxy}"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--proxy-server={proxy}")  # Configure the proxy
    chrome_options.add_argument(
        f"user-agent={get_random_user_agent()}"
    )  # Rotate user agent

    # Set up Chrome driver
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"Debug - Using proxy: {proxy}")
        driver.get(url)

        # Wait for page to load
        random_delay(3, 5)  # Random delay between 3 to 5 seconds

        # Check if the quotes are loaded and print page source for debugging
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print("Debug - Page source loaded")
        print(driver.page_source)  # Print the page source to confirm content structure

        # Attempt to locate quotes by checking for 'div' tags with class 'quote'
        quotes = [
            {
                "text": (
                    quote.find("span", class_="text").get_text()
                    if quote.find("span", class_="text")
                    else ""
                ),
                "author": (
                    quote.find("small", class_="author").get_text()
                    if quote.find("small", class_="author")
                    else ""
                ),
            }
            for quote in soup.find_all("div", class_="quote")
        ]

        # Check if any quotes were found
        if not quotes:
            print(
                "No quotes found. Check if the structure of HTML matches the selector."
            )

        return {"quotes": quotes}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    result = scrape_data()
    print(result)
