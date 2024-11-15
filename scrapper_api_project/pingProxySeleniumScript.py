# pingProxySeleniumScript.py


from selenium import webdriver
from selenium.webdriver.chrome.options import Options


proxy = "http://103.216.82.153:6666"  # Example proxy

chrome_options = Options()
chrome_options.add_argument(f"--proxy-server={proxy}")
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("http://www.whatsmyip.org/")  # Check if IP is shown
    print("Loaded page with proxy successfully.")
except Exception as e:
    print(f"Proxy failed: {e}")
finally:
    driver.quit()
