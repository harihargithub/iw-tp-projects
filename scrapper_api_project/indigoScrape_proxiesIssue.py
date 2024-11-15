# indigoScrape.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    url = "https://www.goindigo.in/flight-booking.html?linkNav=Flight%7CBook%7CBook"

    # Set up proxy
    proxy = get_random_proxy()
    proxy_options = Proxy()
    proxy_options.proxy_type = ProxyType.MANUAL
    proxy_options.http_proxy = f"http://{proxy}"
    proxy_options.ssl_proxy = f"https://{proxy}"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--ignore-certificate-errors"
    )  # Ignore SSL certificate errors
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )  # Disable headless detection
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
        random_delay(
            5, 10
        )  # Random delay between 5 to 10 seconds to allow dynamic content to load

        # Interact with the form elements
        try:
            print("Trying to select 'One Way'")
            one_way_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#bar > div.cmp-custom-drop-down > button")
                )
            )
            one_way_button.click()
            print("'One Way' selected")
        except Exception as e:
            print(f"Error selecting 'One Way': {e}")

        try:
            print("Trying to select '1 Pax'")
            pax_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div.cmp-custom-drop-down > button.cmp-custom-drop-down__btn__icon--user",
                    )
                )
            )
            pax_button.click()
            print("'1 Pax' selected")
        except Exception as e:
            print(f"Error selecting '1 Pax': {e}")

        try:
            print("Trying to enter 'From' location")
            from_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.from-destination input")
                )
            )
            from_input.send_keys("MAA")
            random_delay(1, 2)
            from_input.send_keys(Keys.ENTER)
            print("'From' location entered")
        except Exception as e:
            print(f"Error entering 'From' location: {e}")

        try:
            print("Trying to enter 'To' location")
            to_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.to-destination input")
                )
            )
            to_input.send_keys("TRZ")
            random_delay(1, 2)
            to_input.send_keys(Keys.ENTER)
            print("'To' location entered")
        except Exception as e:
            print(f"Error entering 'To' location: {e}")

        try:
            print("Trying to enter 'Travel Dates'")
            date_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.react-datepicker__input-container input")
                )
            )
            date_input.send_keys("30 Nov 2024")
            random_delay(1, 2)
            date_input.send_keys(Keys.ENTER)
            print("'Travel Dates' entered")
        except Exception as e:
            print(f"Error entering 'Travel Dates': {e}")

        try:
            print("Trying to click 'Search Flight'")
            search_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "#container-b9910c1891 > div > div.dynamiccontainer.aem-GridColumn.aem-GridColumn--default--12 > div > div > div > section > div.widget-container > div.widget-container__search-form > button > span",
                    )
                )
            )
            search_button.click()
            print("'Search Flight' clicked")
        except Exception as e:
            print(f"Error clicking 'Search Flight': {e}")

        # Wait for results page to load
        random_delay(5, 10)

        # Check if the content is loaded and print page source for debugging
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print("Debug - Page source loaded")
        print(driver.page_source)  # Print the page source to confirm content structure

        # Attempt to locate content by checking for specific tags
        # Example: Extracting flight details (this will need to be adjusted based on the actual HTML structure)
        flights = [
            {
                "flight_number": (
                    flight.find("span", class_="flight-number").get_text()
                    if flight.find("span", class_="flight-number")
                    else ""
                ),
                "departure_time": (
                    flight.find("span", class_="departure-time").get_text()
                    if flight.find("span", class_="departure-time")
                    else ""
                ),
                "arrival_time": (
                    flight.find("span", class_="arrival-time").get_text()
                    if flight.find("span", class_="arrival-time")
                    else ""
                ),
                "price": (
                    flight.find("span", class_="price").get_text()
                    if flight.find("span", class_="price")
                    else ""
                ),
            }
            for flight in soup.find_all("div", class_="flight-details")
        ]

        # Check if any content was found
        if not flights:
            print(
                "No content found. Check if the structure of HTML matches the selector."
            )

        return {"flights": flights}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    result = scrape_data()
    print(result)
