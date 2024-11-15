# quotes2scrape4
# .py


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import random
import time

# Random User-Agent list
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    # Add more user-agents for randomization
]

# List of proxies (example)
PROXIES = [
    "http://103.216.82.153:6666",
    "http://103.216.82.22:6666",
    "http://103.216.82.29:6666",
    # Add more proxies here if needed
]


def get_random_proxy():
    return random.choice(PROXIES)


def get_random_user_agent():
    return random.choice(USER_AGENTS)


def scrape_data():
    url = "http://quotes.toscrape.com/"

    # Randomly choose a proxy and user-agent
    proxy = get_random_proxy()
    user_agent = get_random_user_agent()

    # Set up Chrome options with proxy and user-agent
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--user-agent={user_agent}")
    chrome_options.add_argument(f"--proxy-server={proxy}")

    # Set up Chrome driver with the modified options
    service = Service("path_to_chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Introduce random delay
        time.sleep(random.uniform(2, 5))

        # Load the webpage
        driver.get(url)

        # Random delay after loading the page
        time.sleep(random.uniform(1, 3))

        # Parse the content
        soup = BeautifulSoup(driver.page_source, "html.parser")
        quotes = [
            {
                "text": quote.find("span", class_="text").get_text(),
                "author": quote.find("small", class_="author").get_text(),
            }
            for quote in soup.find_all("div", class_="quote")
        ]

        return {"quotes": quotes} if quotes else {"error": "No quotes found"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    result = scrape_data()
    print(result)
