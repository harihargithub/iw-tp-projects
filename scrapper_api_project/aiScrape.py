# aiScrape.py

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


def find_shadow_element(driver, js_path):
    return driver.execute_script(f"return {js_path}")


def scrape_ai():
    url = "https://www.airindia.com/?utm_source=google&utm_medium=cpc&utm_campaign=Acquisition_Perform_SEM_Alltraveltype_India_BAU_Prospecting_Brand_Terms_Allrout_Allsector_NullHaul_NullB_Desktop_EM&gclid=CjwKCAiAudG5BhAREiwAWMlSjANH5h1h45UdP8UuUZ8BdB-0WsgcnAMjc7xCPIbQh0QThnZzfhH6nxoCrpQQAvD_BwE"

    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
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

        # Handle cookie consent pop-up
        try:
            print("Checking for cookie consent pop-up")
            accept_cookies_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_cookies_button.click()
            print("Accepted cookies")
        except Exception as e:
            print(f"Cookie consent pop-up not found: {e}")

        # Wait for the main content to load
        try:
            print("Waiting for main content to load")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.ai-tab-group-wrapper")
                )
            )
            print("Main content loaded")
        except Exception as e:
            print(f"Main content not loaded: {e}")

        # Fill in the search form
        try:
            print("Filling in the search form")

            # Select 'One Way' option
            one_way_js_path = 'document.querySelector("#ai-booking-widget > ai-tab-group > ai-tab:nth-child(1) > ai-search-flight > slot-fb > div.ai-search-flight-wrapper > div.ai-search-trip > div > div.ai-search-trip-type > ai-radio-group").shadowRoot.querySelector("#radio0")'
            one_way_button = find_shadow_element(driver, one_way_js_path)
            one_way_button.click()
            print("Selected 'One Way'")

            # Enter 'From' location
            from_js_path = 'document.querySelector("#ai-booking-widget > ai-tab-group > ai-tab:nth-child(1) > ai-search-flight > slot-fb > div.ai-search-flight-wrapper > div.ai-origin-dest-search > ai-origin-destination").shadowRoot.querySelector("#originAutoComplete").shadowRoot.querySelector("div > div > div.ai-input-wrap > input")'
            from_input = find_shadow_element(driver, from_js_path)
            from_input.send_keys("CJB")
            random_delay(1, 2)
            from_input.send_keys(Keys.RETURN)
            print("Entered 'From' location as 'CJB'")
            # Wait for auto-suggestion dropdown to appear and select the correct option
            try:
                from_auto_suggestion = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//li[contains(text(), "Coimbatore International Airport")]',
                        )
                    )
                )
                from_auto_suggestion.click()
                print("Successfully selected 'From' location from suggestions")
            except Exception as e:
                print(f"Error selecting 'From' location: {e}")

            # Enter 'To' location
            to_js_path = 'document.querySelector("#ai-booking-widget > ai-tab-group > ai-tab:nth-child(1) > ai-search-flight > slot-fb > div.ai-search-flight-wrapper > div.ai-origin-dest-search > ai-origin-destination").shadowRoot.querySelector("#destinationAutoComplete").shadowRoot.querySelector("div > div > div.ai-input-wrap > input")'
            to_input = find_shadow_element(driver, to_js_path)
            to_input.send_keys("MAA")
            random_delay(1, 2)
            to_input.send_keys(Keys.RETURN)
            print("Entered 'To' location as 'MAA'")
            # Wait for auto-suggestion dropdown to appear and select the correct option
            try:
                to_auto_suggestion = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//li[contains(text(), "Chennai International Airport")]',
                        )
                    )
                )
                to_auto_suggestion.click()
                print("Successfully selected 'To' location from suggestions")
            except Exception as e:
                print(f"Error selecting 'To' location: {e}")

            # Enter 'Travel Dates'
            date_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "dpFromDate"))
            )
            date_input.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//td[@data-day="11" and @data-month="12" and @data-year="2024"]',
                    )
                )
            ).click()
            print("Entered 'Travel Dates'")

            # Select '1 Adult'
            adult_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.ai-pax-selector-option-desc")
                )
            )
            adult_input.click()
            print("Selected '1 Adult'")

            # Select 'Economy' class
            class_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-index="0"]'))
            )
            class_input.click()
            print("Selected 'Economy' class")

            # Select 'Cash' payment
            payment_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-index="0"]'))
            )
            payment_input.click()
            print("Selected 'Cash' payment")

            # Select 'None' concession type
            concession_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-index="0"]'))
            )
            concession_input.click()
            print("Selected 'None' concession type")

            # Click 'Search Flight' button
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            search_button.click()
            print("Clicked 'Search Flight' button")

        except Exception as e:
            print(f"Error filling in the search form: {e}")

        # Wait for the results page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[contains(@class, "basic-flight-card-layout-left-section-container")]',
                )
            )
        )

        # Scrape flight details
        flights = driver.find_elements(
            By.XPATH,
            '//*[contains(@class, "basic-flight-card-layout-left-section-container")] | //*[contains(@class, "primary")]',
        )
        for flight in flights:
            print(flight.text)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    scrape_ai()
