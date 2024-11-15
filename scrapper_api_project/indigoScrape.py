# indigoScrape.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    url = "https://www.goindigo.in/flight-booking.html?linkNav=Flight%7CBook%7CBook"

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
    chrome_options.add_argument(
        f"user-agent={get_random_user_agent()}"
    )  # Rotate user agent

    # Set up Chrome driver
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
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
                    (By.XPATH, '//*[@id="bar"]/div[1]/button')
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
                    (By.XPATH, '//*[@id="bar"]/div[2]/div[1]/button')
                )
            )
            pax_button.click()
            print("'1 Pax' selected")
        except Exception as e:
            print(f"Error selecting '1 Pax': {e}")

        try:
            print("Trying to select 'Special Fares'")
            special_fares_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="special-fare-container"]/div')
                )
            )
            special_fares_button.click()
            print("'Special Fares' selected")
        except Exception as e:
            print(f"Error selecting 'Special Fares': {e}")

        try:
            print("Trying to enter 'From' location")
            from_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="container-b9910c1891"]/div/div[3]/div/div/div/section/div[1]/div[3]/div[1]/div[1]/input',
                    )
                )
            )
            from_input.send_keys("Chennai (MAA)")
            random_delay(1, 2)
            from_input.send_keys(Keys.ENTER)
            print("'From' location entered")
        except Exception as e:
            print(f"Error entering 'From' location: {e}")

        try:
            print("Trying to enter 'To' location")
            to_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="container-b9910c1891"]/div/div[3]/div/div/div/section/div[1]/div[3]/div[2]/div[1]/input',
                    )
                )
            )
            to_input.send_keys("Tiruchirappalli (TRZ)")
            random_delay(1, 2)
            to_input.send_keys(Keys.ENTER)
            print("'To' location entered")
        except Exception as e:
            print(f"Error entering 'To' location: {e}")

        try:
            print("Trying to enter 'Travel Dates'")
            date_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="travel-dates-container"]/div[1]/div/div/input')
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
                        By.XPATH,
                        '//*[@id="container-b9910c1891"]/div/div[3]/div/div/div/section/div[1]/div[3]/button/span',
                    )
                )
            )
            search_button.click()
            print("'Search Flight' clicked")
        except Exception as e:
            print(f"Error clicking 'Search Flight': {e}")

        # Wait for results page to load
        random_delay(5, 10)

        # Extract flight details
        flights = []
        try:
            flight_sections = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        '//div[contains(@class, "srp-flight-carousel-container__item rounded-1")]',
                    )
                )
            )
            for flight_section in flight_sections:
                try:
                    flight_details = {
                        "flight_number": flight_section.find_element(
                            By.XPATH, './/p[contains(@class, "srp__flight-num")]'
                        ).text,
                        "departure_time": flight_section.find_element(
                            By.XPATH, './/p[contains(@class, "time")]'
                        ).text,
                        "departure_airport": flight_section.find_elements(
                            By.XPATH, './/p[contains(@class, "airport")]'
                        )[0].text,
                        "arrival_time": flight_section.find_element(
                            By.XPATH, './/p[contains(@class, "sh4")]'
                        ).text,
                        "arrival_airport": flight_section.find_elements(
                            By.XPATH, './/p[contains(@class, "airport")]'
                        )[1].text,
                        "duration": flight_section.find_element(
                            By.XPATH,
                            './/div[contains(@class, "skyplus-text text-color body-small-regular")]',
                        ).text,
                        "price": flight_section.find_element(
                            By.XPATH,
                            './/h4[contains(@class, "body-medium-medium text-primary-main")]',
                        ).text,
                    }
                    flights.append(flight_details)
                except Exception as e:
                    print(f"Error extracting flight details: {e}")
        except Exception as e:
            print(f"Error locating flight sections: {e}")

        if not flights:
            print("No flight details found.")
            return {"error": "No flight details found."}

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
