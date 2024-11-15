# quotes2scrape.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time

# Path to your locally downloaded ChromeDriver (assuming it's extracted)
CHROME_DRIVER_PATH = "C:\\Program Files\\chrome\\chromedriver-win64\\chromedriver.exe"  # Adjust if different

# Verify that the ChromeDriver path is correct
if not os.path.exists(CHROME_DRIVER_PATH):
    raise FileNotFoundError(f"ChromeDriver not found at {CHROME_DRIVER_PATH}")


def scrape_data():
    url = "http://quotes.toscrape.com/"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up Chrome driver
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)

        # Wait for page to load
        time.sleep(3)  # Wait for 3 seconds or adjust as needed

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
        return {"error": str(e)}
    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    result = scrape_data()
    print(result)
