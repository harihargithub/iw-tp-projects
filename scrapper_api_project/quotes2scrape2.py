# quotes2scrape2_workingWell.py

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


def get_random_user_agent():
    return random.choice(USER_AGENTS)


def random_delay(min_delay=1, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))


def scrape_data():
    url = "http://quotes.toscrape.com/"

    # Set up proxy
    proxy_ip = "192.252.211.193"  # Example proxy IP
    proxy_port = "4145"  # Example proxy port
    proxy = f"socks4://{proxy_ip}:{proxy_port}"
    proxy_options = Proxy()
    proxy_options.proxy_type = ProxyType.MANUAL
    proxy_options.socks_proxy = proxy

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
